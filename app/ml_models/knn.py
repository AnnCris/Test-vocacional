import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

class CareerKNN:
    """
    Modelo KNN (K-Nearest Neighbors) para encontrar perfiles similares
    """
    
    def __init__(self, n_neighbors=5, model_path=None):
        """
        Inicializa el modelo KNN
        
        Args:
            n_neighbors: Número de vecinos a considerar
            model_path: Ruta al modelo guardado (si existe)
        """
        self.model = None
        self.scaler = StandardScaler()
        self.student_profiles = None
        self.career_recommendations = None
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            self.model = KNeighborsClassifier(
                n_neighbors=n_neighbors,
                weights='distance'  # Ponderar por distancia
            )
    
    def train(self, X, y, student_profiles=None):
        """
        Entrena el modelo con los datos proporcionados
        
        Args:
            X: Características (datos del estudiante + test)
            y: Etiquetas (carreras recomendadas)
            student_profiles: DataFrame con perfiles completos de estudiantes para referencia
        """
        # Guardar perfiles para recomendaciones futuras
        self.student_profiles = student_profiles
        
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
        print(f"Accuracy del modelo KNN: {accuracy:.4f}")
        
        # Almacenar recomendaciones para cada perfil
        if student_profiles is not None:
            self.career_recommendations = {}
            for idx, profile in student_profiles.iterrows():
                student_id = profile.get('student_id')
                if student_id:
                    recommended_career_id = y[idx]
                    self.career_recommendations[student_id] = recommended_career_id
        
        return accuracy
    
    def find_similar_profiles(self, student_data, top_n=5):
        """
        Encuentra perfiles similares al estudiante actual
        
        Args:
            student_data: DataFrame con los datos del estudiante
            top_n: Número de perfiles similares a devolver
            
        Returns:
            list: Lista de tuplas (id_estudiante, similitud)
        """
        if self.model is None or self.student_profiles is None:
            return []
        
        # Normalizar datos
        X = student_data.values
        X_scaled = self.scaler.transform(X)
        
        # Encontrar vecinos más cercanos
        distances, indices = self.model.kneighbors(
            X_scaled, n_neighbors=min(top_n, len(self.student_profiles))
        )
        
        # Convertir distancias a similitud (1 - distancia normalizada)
        max_distance = distances.max()
        similarities = 1 - (distances[0] / max_distance if max_distance > 0 else distances[0])
        
        # Obtener IDs de estudiantes similares
        similar_profiles = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.student_profiles):
                student_id = self.student_profiles.iloc[idx].get('student_id')
                if student_id:
                    similar_profiles.append((student_id, float(similarities[i])))
        
        return similar_profiles
    
    def recommend_careers_by_similar_profiles(self, student_data, top_n=3):
        """
        Recomienda carreras basándose en perfiles similares
        
        Args:
            student_data: DataFrame con los datos del estudiante
            top_n: Número de carreras a recomendar
            
        Returns:
            list: Lista de IDs de carreras recomendadas
        """
        if self.model is None or self.career_recommendations is None:
            return []
        
        # Encontrar perfiles similares
        similar_profiles = self.find_similar_profiles(student_data, top_n=10)
        
        # Contador de frecuencia de carreras recomendadas
        career_counts = {}
        for student_id, similarity in similar_profiles:
            if student_id in self.career_recommendations:
                career_id = self.career_recommendations[student_id]
                if career_id in career_counts:
                    career_counts[career_id] += similarity
                else:
                    career_counts[career_id] = similarity
        
        # Ordenar carreras por frecuencia ponderada por similitud
        recommended_careers = sorted(
            [(career_id, count) for career_id, count in career_counts.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        return recommended_careers[:top_n]
    
    def predict_career_compatibility(self, student_data, career_data):
        """
        Predice la compatibilidad entre un estudiante y varias carreras
        
        Args:
            student_data: DataFrame con los datos del estudiante
            career_data: DataFrame con los datos de las carreras
            
        Returns:
            list: Lista de tuplas (id_carrera, compatibilidad)
        """
        # Si no hay suficientes datos para KNN, usar enfoque basado en reglas
        if self.model is None or self.student_profiles is None or len(self.student_profiles) < 5:
            return self._rule_based_compatibility(student_data, career_data)
        
        # Recomendaciones basadas en perfiles similares
        career_recommendations = self.recommend_careers_by_similar_profiles(student_data, top_n=5)
        
        # Si no hay suficientes recomendaciones, complementar con enfoque basado en reglas
        if len(career_recommendations) < 3:
            rule_based = self._rule_based_compatibility(student_data, career_data)
            
            # Fusionar recomendaciones evitando duplicados
            recommended_ids = [c[0] for c in career_recommendations]
            for career_id, score in rule_based:
                if career_id not in recommended_ids:
                    career_recommendations.append((career_id, score * 0.8))  # Dar menos peso a las reglas
                    recommended_ids.append(career_id)
                    
                    if len(career_recommendations) >= 5:
                        break
        
        # Ordenar por compatibilidad
        career_recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return career_recommendations
    
    def _rule_based_compatibility(self, student_data, career_data):
        """
        Calcula compatibilidad usando reglas cuando no hay suficientes datos para KNN
        """
        results = []
        
        # Extraer puntajes del test
        chaside_areas = ['c', 'h', 'a', 's', 'i', 'd', 'e']
        student_scores = {
            area: student_data[f'score_{area}'].values[0]
            for area in chaside_areas
        }
        
        # Encontrar áreas más fuertes
        top_areas = sorted(student_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Calcular compatibilidad con cada carrera
        for _, career in career_data.iterrows():
            compatibility = 0.0
            
            # Para cada área top, calcular compatibilidad
            for area, score in top_areas:
                career_area_score = career[f'area_{area}']
                compatibility += career_area_score * score
            
            # Normalizar (0-1)
            max_possible = sum(score for _, score in top_areas)
            if max_possible > 0:
                compatibility /= max_possible
            
            results.append((int(career['id']), float(compatibility)))
        
        # Ordenar por compatibilidad
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results
    
    def save_model(self, model_path):
        """Guarda el modelo entrenado en un archivo"""
        if self.model is not None:
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler,
                'student_profiles': self.student_profiles,
                'career_recommendations': self.career_recommendations
            }, model_path)
            print(f"Modelo KNN guardado en {model_path}")
    
    def load_model(self, model_path):
        """Carga un modelo previamente guardado"""
        if os.path.exists(model_path):
            data = joblib.load(model_path)
            self.model = data['model']
            self.scaler = data['scaler']
            self.student_profiles = data.get('student_profiles')
            self.career_recommendations = data.get('career_recommendations')
            print(f"Modelo KNN cargado desde {model_path}")