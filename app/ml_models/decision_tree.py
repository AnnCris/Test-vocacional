import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import joblib
import os

class CareerDecisionTree:
    """
    Modelo de árbol de decisión para clasificar estudiantes según sus carreras ideales
    """
    
    def __init__(self, model_path=None):
        """
        Inicializa el modelo de árbol de decisión
        
        Args:
            model_path: Ruta al modelo guardado (si existe)
        """
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = None
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            self.model = DecisionTreeClassifier(
                max_depth=5,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            )
    
    def train(self, X, y, feature_names=None):
        """
        Entrena el modelo con los datos proporcionados
        
        Args:
            X: Características (datos del estudiante + test)
            y: Etiquetas (carreras recomendadas)
            feature_names: Nombres de las características para visualización
        """
        # Guardar nombres de características
        self.feature_names = feature_names if feature_names else [f"feature_{i}" for i in range(X.shape[1])]
        
        # Normalizar datos
        X_scaled = self.scaler.fit_transform(X)
        
        # Dividir datos en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        # Entrenar modelo
        self.model.fit(X_train, y_train)
        
        # Evaluar modelo
        accuracy = self.model.score(X_test, y_test)
        print(f"Accuracy del modelo de árbol de decisión: {accuracy:.4f}")
        
        return accuracy
    
    def predict_best_careers(self, student_data, career_data, top_n=5):
        """
        Predice las mejores carreras para un estudiante
        
        Args:
            student_data: DataFrame con los datos del estudiante
            career_data: DataFrame con los datos de las carreras
            top_n: Número de carreras a recomendar
            
        Returns:
            list: Lista de tuplas (id_carrera, probabilidad)
        """
        if self.model is None:
            # Si no hay modelo entrenado, usamos un enfoque basado en reglas
            return self._rule_based_prediction(student_data, career_data, top_n)
        
        # Extraer características relevantes del estudiante
        X = student_data.values
        
        # Normalizar datos
        X_scaled = self.scaler.transform(X)
        
        # Obtener probabilidades para cada clase (carrera)
        probas = self.model.predict_proba(X_scaled)[0]
        
        # Mapear probabilidades a carreras
        career_probas = []
        for i, proba in enumerate(probas):
            if i < len(career_data):
                career_id = career_data.iloc[i]['id']
                career_probas.append((int(career_id), float(proba)))
        
        # Ordenar por probabilidad (descendente)
        career_probas.sort(key=lambda x: x[1], reverse=True)
        
        return career_probas[:top_n]
    
    def _rule_based_prediction(self, student_data, career_data, top_n=5):
        """
        Implementa un enfoque basado en reglas cuando no hay modelo entrenado
        """
        # Obtener puntajes del test CHASIDE
        chaside_scores = {
            'score_c': student_data['score_c'].values[0],
            'score_h': student_data['score_h'].values[0],
            'score_a': student_data['score_a'].values[0],
            'score_s': student_data['score_s'].values[0],
            'score_i': student_data['score_i'].values[0],
            'score_d': student_data['score_d'].values[0],
            'score_e': student_data['score_e'].values[0]
        }
        
        # Identificar las dos áreas con mayor puntaje
        top_areas = sorted(chaside_scores.items(), key=lambda x: x[1], reverse=True)[:2]
        
        # Calcular compatibilidad con cada carrera
        results = []
        for _, career in career_data.iterrows():
            score = 0.0
            
            # Compatibilidad basada en áreas CHASIDE
            for area, area_score in top_areas:
                # Extraer la letra del área del nombre del puntaje (ej: 'score_c' -> 'c')
                area_letter = area[-1]  
                career_area_value = career[f'area_{area_letter}']
                score += career_area_value * area_score
            
            # Compatibilidad basada en materias académicas
            academic_subjects = {
                'math_score': student_data['math_score'].values[0],
                'science_score': student_data['science_score'].values[0],
                'language_score': student_data['language_score'].values[0],
                'social_science_score': student_data['social_science_score'].values[0],
                'arts_score': student_data['arts_score'].values[0]
            }
            
            # Mapeo de áreas a materias relacionadas
            area_subject_mapping = {
                'c': ['math_score', 'social_science_score'],
                'h': ['language_score', 'social_science_score'],
                'a': ['arts_score', 'language_score'],
                's': ['science_score', 'math_score'],
                'i': ['math_score', 'science_score'],
                'd': ['social_science_score', 'math_score'],
                'e': ['science_score', 'math_score']
            }
            
            # Para cada área top, considerar materias relacionadas
            for area, _ in top_areas:
                area_letter = area[-1]
                relevant_subjects = area_subject_mapping.get(area_letter, [])
                for subject in relevant_subjects:
                    subject_score = academic_subjects.get(subject, 0)
                    score += 0.2 * subject_score  # Peso menor que el test CHASIDE
            
            # Normalizar score (0-1)
            max_possible_score = 2 * 10 + 4 * 10 * 0.2  # 2 áreas + 4 materias con peso 0.2
            score = min(score / max_possible_score, 1.0)
            
            results.append((int(career['id']), float(score)))
        
        # Ordenar por puntaje
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:top_n]
    
    def visualize_tree(self, path='tree.png'):
        """
        Visualiza el árbol de decisión entrenado
        
        Args:
            path: Ruta donde guardar la imagen
        """
        if self.model is None:
            print("No hay modelo entrenado para visualizar")
            return
        
        plt.figure(figsize=(20, 10))
        plot_tree(
            self.model, 
            feature_names=self.feature_names,
            filled=True, 
            rounded=True
        )
        plt.savefig(path)
        print(f"Árbol guardado en {path}")
    
    def get_feature_importance(self):
        """
        Obtiene la importancia de cada característica en el modelo
        
        Returns:
            dict: Diccionario con la importancia de cada característica
        """
        if self.model is None or self.feature_names is None:
            return {}
        
        importances = self.model.feature_importances_
        return {
            feature: importance
            for feature, importance in zip(self.feature_names, importances)
        }
    
    def save_model(self, model_path):
        """Guarda el modelo entrenado en un archivo"""
        if self.model is not None:
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_names': self.feature_names
            }, model_path)
            print(f"Modelo guardado en {model_path}")
    
    def load_model(self, model_path):
        """Carga un modelo previamente guardado"""
        if os.path.exists(model_path):
            data = joblib.load(model_path)
            self.model = data['model']
            self.scaler = data['scaler']
            self.feature_names = data['feature_names']
            print(f"Modelo cargado desde {model_path}")