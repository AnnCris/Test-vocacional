import numpy as np
import pandas as pd
from app.ml_models.logistic_regression import CareerLogisticRegression
from app.ml_models.decision_tree import CareerDecisionTree
from app.ml_models.knn import CareerKNN
from app.ml_models.neural_network import CareerNeuralNetwork

class EnsembleRecommender:
    """
    Sistema de recomendación de carreras que combina varios modelos
    para obtener recomendaciones más robustas y precisas
    """
    
    def __init__(self):
        """Inicializa el sistema de recomendación con múltiples modelos"""
        self.logistic_model = CareerLogisticRegression()
        self.tree_model = CareerDecisionTree()
        self.knn_model = CareerKNN(n_neighbors=5)
        self.nn_model = CareerNeuralNetwork()
        
        # Pesos para cada modelo en el ensemble
        self.model_weights = {
            'logistic': 0.25,
            'tree': 0.25,
            'knn': 0.25,
            'nn': 0.25
        }
        
        # Métricas de precisión para ajustar pesos dinámicamente
        self.model_accuracies = {
            'logistic': 0.0,
            'tree': 0.0,
            'knn': 0.0,
            'nn': 0.0
        }
    
    def train_models(self, X, y, student_profiles=None):
        """
        Entrena todos los modelos con los mismos datos
        
        Args:
            X: Características de entrenamiento
            y: Etiquetas (carreras recomendadas)
            student_profiles: Perfiles completos de estudiantes (para KNN)
        """
        # Entrenar cada modelo y registrar su precisión
        acc_logistic = self.logistic_model.train(X, y)
        acc_tree = self.tree_model.train(X, y)
        acc_knn = self.knn_model.train(X, y, student_profiles)
        acc_nn = self.nn_model.train(X, y)
        
        # Actualizar métricas de precisión
        self.model_accuracies = {
            'logistic': acc_logistic,
            'tree': acc_tree,
            'knn': acc_knn,
            'nn': acc_nn
        }
        
        # Ajustar pesos según precisión
        self._adjust_weights_by_accuracy()
        
        print(f"Ensemble entrenado con éxito. Pesos de modelos: {self.model_weights}")
    
    def _adjust_weights_by_accuracy(self):
        """Ajusta los pesos de los modelos según su precisión"""
        total_acc = sum(self.model_accuracies.values())
        
        if total_acc > 0:
            for model, acc in self.model_accuracies.items():
                self.model_weights[model] = acc / total_acc
    
    def recommend_careers(self, student_data, career_data, top_n=5):
        """
        Genera recomendaciones combinando los resultados de todos los modelos
        
        Args:
            student_data: DataFrame con los datos del estudiante
            career_data: DataFrame con los datos de las carreras
            top_n: Número de carreras a recomendar
            
        Returns:
            list: Lista de tuplas (id_carrera, puntuación, modelo_principal)
        """
        # Obtener recomendaciones de cada modelo
        logistic_recs = self.logistic_model.predict_compatibility(student_data, career_data)
        tree_recs = self.tree_model.predict_best_careers(student_data, career_data)
        knn_recs = self.knn_model.predict_career_compatibility(student_data, career_data)
        nn_recs = self.nn_model.predict_career_compatibility(student_data, career_data)
        
        # Combinar recomendaciones con pesos
        combined_scores = {}
        model_contributions = {}
        
        # Procesar recomendaciones de regresión logística
        for career_id, score in logistic_recs:
            combined_scores[career_id] = score * self.model_weights['logistic']
            model_contributions[career_id] = {'logistic': score}
        
        # Procesar recomendaciones de árbol de decisión
        for career_id, score in tree_recs:
            if career_id in combined_scores:
                combined_scores[career_id] += score * self.model_weights['tree']
                model_contributions[career_id]['tree'] = score
            else:
                combined_scores[career_id] = score * self.model_weights['tree']
                model_contributions[career_id] = {'tree': score}
        
        # Procesar recomendaciones de KNN
        for career_id, score in knn_recs:
            if career_id in combined_scores:
                combined_scores[career_id] += score * self.model_weights['knn']
                model_contributions[career_id]['knn'] = score
            else:
                combined_scores[career_id] = score * self.model_weights['knn']
                model_contributions[career_id] = {'knn': score}
        
        # Procesar recomendaciones de red neuronal
        for career_id, score in nn_recs:
            if career_id in combined_scores:
                combined_scores[career_id] += score * self.model_weights['nn']
                model_contributions[career_id]['nn'] = score
            else:
                combined_scores[career_id] = score * self.model_weights['nn']
                model_contributions[career_id] = {'nn': score}
        
        # Determinar el modelo que más contribuyó a cada carrera
        main_models = {}
        for career_id, contributions in model_contributions.items():
            main_model = max(contributions.items(), key=lambda x: x[1])[0]
            main_models[career_id] = main_model
        
        # Preparar resultados ordenados por puntuación
        results = []
        for career_id, score in combined_scores.items():
            main_model = main_models.get(career_id, 'ensemble')
            results.append((int(career_id), float(score), main_model))
        
        # Ordenar por puntuación descendente
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:top_n]
    
    def generate_detailed_recommendation(self, student_data, career_data, test_answers):
        """
        Genera una recomendación detallada con explicaciones
        
        Args:
            student_data: DataFrame con los datos del estudiante
            career_data: DataFrame con los datos de las carreras
            test_answers: Objeto TestAnswer con las respuestas del test
            
        Returns:
            dict: Diccionario con recomendaciones detalladas
        """
        # Obtener recomendaciones básicas
        top_recommendations = self.recommend_careers(student_data, career_data, top_n=3)
        
        # Preparar resultados detallados
        detailed_results = []
        
        for career_id, score, main_model in top_recommendations:
            # Buscar la carrera en los datos
            career = career_data[career_data['id'] == career_id].iloc[0]
            
            # Extraer áreas CHASIDE más relevantes para esta carrera
            career_areas = {
                'C': career['area_c'],
                'H': career['area_h'],
                'A': career['area_a'],
                'S': career['area_s'],
                'I': career['area_i'],
                'D': career['area_d'],
                'E': career['area_e']
            }
            
            top_areas = sorted(career_areas.items(), key=lambda x: x[1], reverse=True)[:3]
            
            # Extraer puntajes del estudiante en esas áreas
            student_scores = {
                'C': test_answers.score_c,
                'H': test_answers.score_h,
                'A': test_answers.score_a,
                'S': test_answers.score_s,
                'I': test_answers.score_i,
                'D': test_answers.score_d,
                'E': test_answers.score_e
            }
            
            # Generar explicación
            strengths = []
            
            for area, career_score in top_areas:
                if career_score > 0.5:  # Solo considerar áreas relevantes
                    student_score = student_scores[area]
                    match_percentage = min(student_score * 10, 100)  # Convertir a porcentaje
                    
                    area_names = {
                        'C': 'Administrativas y contables',
                        'H': 'Humanísticas y sociales',
                        'A': 'Artísticas',
                        'S': 'Ciencias de la salud',
                        'I': 'Ingeniería y computación',
                        'D': 'Defensa y seguridad',
                        'E': 'Ciencias exactas y naturales'
                    }
                    
                    area_name = area_names.get(area, area)
                    
                    if match_percentage > 60:
                        strengths.append({
                            'area': area,
                            'area_name': area_name,
                            'match_percentage': match_percentage,
                            'importance': career_score * 100  # Convertir a porcentaje
                        })
            
            # Preparar detalle de la recomendación
            detail = {
                'career_id': int(career_id),
                'career_name': career['name'],
                'compatibility_score': float(score) * 100,  # Convertir a porcentaje
                'main_model': main_model,
                'strengths': strengths,
                'recommended_areas': [{'area': area, 'importance': score * 100} for area, score in top_areas]
            }
            
            detailed_results.append(detail)
        
        return {
            'recommendations': detailed_results,
            'model_weights': self.model_weights
        }
    
    def save_models(self, base_path):
        """Guarda todos los modelos entrenados"""
        self.logistic_model.save_model(f"{base_path}/logistic_model.pkl")
        self.tree_model.save_model(f"{base_path}/tree_model.pkl")
        self.knn_model.save_model(f"{base_path}/knn_model.pkl")
        self.nn_model.save_model(f"{base_path}/nn_model.pkl")
    
    def load_models(self, base_path):
        """Carga todos los modelos previamente guardados"""
        self.logistic_model.load_model(f"{base_path}/logistic_model.pkl")
        self.tree_model.load_model(f"{base_path}/tree_model.pkl")
        self.knn_model.load_model(f"{base_path}/knn_model.pkl")
        self.nn_model.load_model(f"{base_path}/nn_model.pkl")