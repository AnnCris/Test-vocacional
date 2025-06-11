import numpy as np
import pandas as pd
import os
import warnings

# Configurar para evitar errores en Windows
os.environ['LOKY_MAX_CPU_COUNT'] = '2'
warnings.filterwarnings('ignore', category=UserWarning)

class EnsembleRecommender:
    """
    Sistema de recomendación de carreras que combina varios modelos
    para obtener recomendaciones más robustas y precisas - CORREGIDO
    """
    
    def __init__(self):
        """Inicializa el sistema de recomendación con múltiples modelos"""
        self.models = {}
        self.model_weights = {}
        self.model_accuracies = {}
        
        # Intentar importar modelos con manejo de errores
        self._initialize_models()
    
    def _initialize_models(self):
        """Inicializa modelos disponibles con manejo de errores"""
        try:
            from app.ml_models.logistic_regression import CareerLogisticRegression
            self.models['logistic'] = CareerLogisticRegression()
            print("✅ Regresión Logística disponible")
        except Exception as e:
            print(f"⚠️ Regresión Logística no disponible: {e}")
        
        try:
            from app.ml_models.decision_tree import CareerDecisionTree
            self.models['tree'] = CareerDecisionTree()
            print("✅ Árbol de Decisión disponible")
        except Exception as e:
            print(f"⚠️ Árbol de Decisión no disponible: {e}")
        
        try:
            from app.ml_models.knn import CareerKNN
            self.models['knn'] = CareerKNN(n_neighbors=3)  # Reducir vecinos
            print("✅ KNN disponible")
        except Exception as e:
            print(f"⚠️ KNN no disponible: {e}")
        
        # Nota: Omitimos red neuronal por simplicidad y estabilidad
        print(f"📊 {len(self.models)} modelos inicializados")
        
        # Inicializar pesos uniformes
        if self.models:
            weight = 1.0 / len(self.models)
            self.model_weights = {name: weight for name in self.models.keys()}
            self.model_accuracies = {name: 0.0 for name in self.models.keys()}
    
    def train_models(self, X, y, student_profiles=None):
        """
        Entrena todos los modelos disponibles con manejo robusto de errores
        
        Args:
            X: Características de entrenamiento
            y: Etiquetas (carreras recomendadas)
            student_profiles: Perfiles completos de estudiantes (para KNN)
        """
        if not self.models:
            print("❌ No hay modelos disponibles para entrenar")
            return False
        
        print(f"🔄 Entrenando {len(self.models)} modelos...")
        
        successful_models = 0
        
        # Entrenar cada modelo individualmente
        for model_name, model in self.models.items():
            try:
                print(f"   📈 Entrenando {model_name}...")
                
                if model_name == 'knn' and student_profiles is not None:
                    # KNN necesita perfiles de estudiantes
                    accuracy = model.train(X, y, student_profiles)
                else:
                    # Otros modelos solo necesitan X, y
                    accuracy = model.train(X, y)
                
                self.model_accuracies[model_name] = accuracy
                successful_models += 1
                print(f"   ✅ {model_name}: {accuracy:.2%}")
                
            except Exception as e:
                print(f"   ❌ Error entrenando {model_name}: {e}")
                # Remover modelo fallido
                if model_name in self.model_accuracies:
                    del self.model_accuracies[model_name]
                continue
        
        if successful_models == 0:
            print("❌ No se pudo entrenar ningún modelo")
            return False
        
        # Ajustar pesos según precisión de modelos exitosos
        self._adjust_weights_by_accuracy()
        
        print(f"✅ {successful_models}/{len(self.models)} modelos entrenados exitosamente")
        print(f"🎯 Pesos finales: {self.model_weights}")
        
        return True
    
    def _adjust_weights_by_accuracy(self):
        """Ajusta los pesos de los modelos según su precisión"""
        # Solo considerar modelos que se entrenaron exitosamente
        valid_accuracies = {name: acc for name, acc in self.model_accuracies.items() if acc > 0}
        
        if not valid_accuracies:
            return
        
        total_acc = sum(valid_accuracies.values())
        
        if total_acc > 0:
            # Actualizar pesos solo para modelos válidos
            self.model_weights = {name: acc / total_acc for name, acc in valid_accuracies.items()}
        else:
            # Si todas las precisiones son 0, usar pesos uniformes
            weight = 1.0 / len(valid_accuracies)
            self.model_weights = {name: weight for name in valid_accuracies.keys()}
    
    def recommend_careers(self, student_data, career_data, top_n=5):
        """
        Genera recomendaciones combinando los resultados de modelos disponibles
        
        Args:
            student_data: DataFrame con los datos del estudiante
            career_data: DataFrame con los datos de las carreras
            top_n: Número de carreras a recomendar
            
        Returns:
            list: Lista de tuplas (id_carrera, puntuación, modelo_principal)
        """
        if not self.models or not self.model_weights:
            print("⚠️ No hay modelos entrenados disponibles")
            return []
        
        # Obtener recomendaciones de cada modelo disponible
        all_recommendations = {}
        model_contributions = {}
        
        for model_name, model in self.models.items():
            if model_name not in self.model_weights:
                continue  # Saltar modelos que fallaron en entrenamiento
            
            try:
                print(f"🔄 Obteniendo recomendaciones de {model_name}...")
                
                if model_name == 'logistic':
                    recommendations = model.predict_compatibility(student_data, career_data)
                elif model_name == 'tree':
                    recommendations = model.predict_best_careers(student_data, career_data, top_n=top_n*2)
                elif model_name == 'knn':
                    recommendations = model.predict_career_compatibility(student_data, career_data)
                else:
                    continue
                
                # Procesar recomendaciones
                weight = self.model_weights[model_name]
                
                for career_id, score in recommendations[:top_n*2]:  # Considerar más carreras
                    if career_id in all_recommendations:
                        all_recommendations[career_id] += score * weight
                        model_contributions[career_id][model_name] = score
                    else:
                        all_recommendations[career_id] = score * weight
                        model_contributions[career_id] = {model_name: score}
                
                print(f"   ✅ {len(recommendations)} recomendaciones de {model_name}")
                
            except Exception as e:
                print(f"   ❌ Error obteniendo recomendaciones de {model_name}: {e}")
                continue
        
        if not all_recommendations:
            print("⚠️ No se obtuvieron recomendaciones de ningún modelo")
            return []
        
        # Determinar el modelo que más contribuyó a cada carrera
        main_models = {}
        for career_id, contributions in model_contributions.items():
            if contributions:
                main_model = max(contributions.items(), key=lambda x: x[1])[0]
                main_models[career_id] = main_model
            else:
                main_models[career_id] = 'ensemble'
        
        # Preparar resultados ordenados por puntuación
        results = []
        for career_id, score in all_recommendations.items():
            main_model = main_models.get(career_id, 'ensemble')
            results.append((int(career_id), float(score), main_model))
        
        # Ordenar por puntuación descendente
        results.sort(key=lambda x: x[1], reverse=True)
        
        print(f"✅ {len(results)} recomendaciones combinadas generadas")
        return results[:top_n]
    
    def save_models(self, base_path):
        """Guarda todos los modelos entrenados exitosamente"""
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        
        saved_count = 0
        
        for model_name, model in self.models.items():
            if model_name in self.model_accuracies and self.model_accuracies[model_name] > 0:
                try:
                    model_file = os.path.join(base_path, f"{model_name}_model.pkl")
                    model.save_model(model_file)
                    saved_count += 1
                    print(f"💾 Modelo {model_name} guardado")
                except Exception as e:
                    print(f"⚠️ Error guardando {model_name}: {e}")
        
        print(f"✅ {saved_count} modelos guardados en {base_path}")
    
    def load_models(self, base_path):
        """Carga todos los modelos previamente guardados"""
        if not os.path.exists(base_path):
            print(f"⚠️ Directorio de modelos no existe: {base_path}")
            return False
        
        loaded_count = 0
        
        for model_name in list(self.models.keys()):
            model_file = os.path.join(base_path, f"{model_name}_model.pkl")
            if os.path.exists(model_file):
                try:
                    self.models[model_name].load_model(model_file)
                    loaded_count += 1
                    print(f"📂 Modelo {model_name} cargado")
                except Exception as e:
                    print(f"⚠️ Error cargando {model_name}: {e}")
                    # Remover modelo que no se pudo cargar
                    del self.models[model_name]
        
        if loaded_count > 0:
            # Reajustar pesos para modelos cargados
            weight = 1.0 / len(self.models)
            self.model_weights = {name: weight for name in self.models.keys()}
            print(f"✅ {loaded_count} modelos cargados exitosamente")
            return True
        else:
            print("⚠️ No se pudieron cargar modelos")
            return False