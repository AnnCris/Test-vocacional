import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

class CareerNeuralNetwork:
    """
    Modelo de Red Neuronal para predecir carreras adecuadas basadas en perfiles complejos
    """
    
    def __init__(self, model_path=None):
        """
        Inicializa el modelo de red neuronal
        
        Args:
            model_path: Ruta al modelo guardado (si existe)
        """
        self.model = None
        self.scaler = StandardScaler()
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            # Arquitectura de la red: capa de entrada, dos capas ocultas, capa de salida
            self.model = MLPClassifier(
                hidden_layer_sizes=(64, 32),  # Dos capas ocultas de 64 y 32 neuronas
                activation='relu',             # Función de activación ReLU
                solver='adam',                 # Optimizador Adam
                alpha=0.0001,                  # Término de regularización
                batch_size='auto',             # Tamaño del batch automático
                learning_rate='adaptive',      # Tasa de aprendizaje adaptativo
                max_iter=1000,                 # Máximo de iteraciones
                random_state=42                # Semilla aleatoria para reproducibilidad
            )
    
    def train(self, X, y):
        """
        Entrena el modelo de red neuronal con los datos proporcionados
        
        Args:
            X: Características (datos del estudiante + test)
            y: Etiquetas (carreras recomendadas)
            
        Returns:
            float: Precisión del modelo
        """
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
        print(f"Precisión del modelo de red neuronal: {accuracy:.4f}")
        
        return accuracy
    
    def predict_careers(self, student_data, career_ids, top_n=5):
        """
        Predice las carreras más adecuadas para un estudiante
        
        Args:
            student_data: DataFrame con los datos del estudiante
            career_ids: Lista de IDs de carreras disponibles
            top_n: Número de carreras a recomendar
            
        Returns:
            list: Lista de tuplas (id_carrera, probabilidad)
        """
        if self.model is None:
            # Si no hay modelo entrenado, usar enfoque basado en reglas
            return self._rule_based_prediction(student_data, top_n)
        
        # Normalizar datos
        X = self.scaler.transform(student_data.values)
        
        # Obtener probabilidades para cada clase
        probas = self.model.predict_proba(X)[0]
        
        # Mapear clases a carreras y sus probabilidades
        career_probas = []
        
        for i, label in enumerate(self.model.classes_):
            if i < len(career_ids):
                career_id = career_ids[i]
                probability = probas[i]
                career_probas.append((career_id, float(probability)))
        
        # Ordenar por probabilidad descendente
        career_probas.sort(key=lambda x: x[1], reverse=True)
        
        return career_probas[:top_n]
    
    def predict_career_compatibility(self, student_data, career_data):
        """
        Calcula la compatibilidad entre un estudiante y varias carreras
        
        Args:
            student_data: DataFrame con los datos del estudiante
            career_data: DataFrame con los datos de las carreras
            
        Returns:
            list: Lista de tuplas (id_carrera, compatibilidad)
        """
        # Si no hay modelo entrenado o no hay suficientes datos
        if self.model is None or len(student_data) == 0:
            return self._rule_based_compatibility(student_data, career_data)
        
        results = []
        
        # Normalizar datos del estudiante
        student_scaled = self.scaler.transform(student_data.values)
        
        # Para cada carrera, calcular el score de compatibilidad
        for _, career in career_data.iterrows():
            career_id = int(career['id'])
            
            # Extraer características de la carrera
            career_features = [
                career['area_c'],
                career['area_h'],
                career['area_a'],
                career['area_s'],
                career['area_i'],
                career['area_d'],
                career['area_e']
            ]
            
            # Concatenar datos del estudiante con los de la carrera
            # (Simulando una entrada combinada para el modelo)
            X_combined = np.concatenate([student_scaled[0], career_features])
            X_combined = X_combined.reshape(1, -1)
            
            # Predecir "probabilidad" de compatibilidad
            # (En realidad estamos usando un truco ya que la red no está entrenada para esto)
            compatibility = self._calculate_custom_compatibility(student_data, career)
            
            results.append((career_id, float(compatibility)))
        
        # Ordenar por compatibilidad
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results
    
    def _calculate_custom_compatibility(self, student_data, career):
        """
        Calcula una puntuación de compatibilidad personalizada
        """
        # Extraer puntajes CHASIDE del estudiante
        chaside_areas = ['c', 'h', 'a', 's', 'i', 'd', 'e']
        student_scores = {
            area: student_data[f'score_{area}'].values[0]
            for area in chaside_areas
        }
        
        # Calcular compatibilidad ponderada por áreas
        compatibility = 0.0
        total_weight = 0.0
        
        for area in chaside_areas:
            student_score = student_scores[area]
            career_score = career[f'area_{area}']
            
            # Dar más peso a las áreas con mayor puntaje
            weight = 1.0 + (student_score * 0.5)
            compatibility += weight * student_score * career_score
            total_weight += weight
        
        # Normalizar (0-1)
        if total_weight > 0:
            compatibility /= total_weight
        
        return compatibility
    
    def _rule_based_compatibility(self, student_data, career_data):
        """
        Calcula compatibilidad usando reglas cuando no hay modelo entrenado
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
    
    def _rule_based_prediction(self, student_data, top_n=5):
        """
        Implementa un enfoque basado en reglas cuando no hay modelo entrenado
        
        Args:
            student_data: DataFrame con los datos del estudiante
            top_n: Número de carreras a recomendar
            
        Returns:
            list: Lista de IDs de carreras recomendadas
        """
        # Este método debería implementarse con una lógica específica
        # para cada caso de uso. Por ahora, devolvemos una lista vacía.
        return []
    
    def save_model(self, model_path):
        """Guarda el modelo entrenado en un archivo"""
        if self.model is not None:
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler
            }, model_path)
            print(f"Modelo de red neuronal guardado en {model_path}")
    
    def load_model(self, model_path):
        """Carga un modelo previamente guardado"""
        if os.path.exists(model_path):
            data = joblib.load(model_path)
            self.model = data['model']
            self.scaler = data['scaler']
            print(f"Modelo de red neuronal cargado desde {model_path}")