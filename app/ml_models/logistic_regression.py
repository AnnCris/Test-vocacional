import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

class CareerLogisticRegression:
    """
    Modelo de regresión logística para predecir la compatibilidad de carreras
    """
    
    def __init__(self, model_path=None):
        """
        Inicializa el modelo de regresión logística
        
        Args:
            model_path: Ruta al modelo guardado (si existe)
        """
        self.model = None
        self.scaler = StandardScaler()
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            self.model = LogisticRegression(multi_class='ovr', max_iter=1000)
    
    def train(self, X, y):
        """
        Entrena el modelo con los datos proporcionados
        
        Args:
            X: Características (datos del estudiante + test)
            y: Etiquetas (carreras recomendadas)
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
        print(f"Accuracy del modelo de regresión logística: {accuracy:.4f}")
        
        return accuracy
    
    def predict_compatibility(self, student_data, career_data):
        """
        Predice la compatibilidad entre un estudiante y varias carreras
        
        Args:
            student_data: DataFrame con los datos del estudiante
            career_data: DataFrame con los datos de las carreras
            
        Returns:
            list: Lista de tuplas (id_carrera, probabilidad)
        """
        if self.model is None:
            # Si no hay modelo entrenado, usamos un enfoque basado en reglas
            return self._rule_based_prediction(student_data, career_data)
        
        # Preparar datos para predicción
        results = []
        
        # Para cada carrera, crear un vector de características combinando estudiante y carrera
        for _, career_row in career_data.iterrows():
            career_id = int(career_row['id'])
            
            # Combinar características de estudiante y carrera
            features = self._combine_features(student_data, career_row)
            
            # Aplicar el escalador
            features_scaled = self.scaler.transform(features)
            
            # Predecir probabilidad
            proba = self.model.predict_proba(features_scaled)[0, 1]  # Probabilidad de clase positiva
            
            results.append((career_id, float(proba)))
        
        # Ordenar por probabilidad (descendente)
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results
    
    def _combine_features(self, student_data, career_row):
        """Combina las características del estudiante y la carrera"""
        # Excluir el ID de carrera para la predicción
        career_features = career_row.drop('id')
        
        # Crear una matriz de características combinadas
        combined = pd.DataFrame()
        
        # Repetir los datos del estudiante para cada carrera
        for col in student_data.columns:
            combined[col] = student_data[col].values
        
        # Agregar características de la carrera
        for col in career_features.index:
            combined[f'career_{col}'] = career_features[col]
        
        return combined
    
    def _rule_based_prediction(self, student_data, career_data):
        """
        Implementa un enfoque basado en reglas cuando no hay modelo entrenado
        
        Este método se usa cuando no hay suficientes datos para entrenar un modelo ML.
        """
        results = []
        
        # Normalizar puntajes del test para comparar
        test_scores = {
            'c': student_data['score_c'].values[0],
            'h': student_data['score_h'].values[0],
            'a': student_data['score_a'].values[0],
            's': student_data['score_s'].values[0], 
            'i': student_data['score_i'].values[0],
            'd': student_data['score_d'].values[0],
            'e': student_data['score_e'].values[0]
        }
        
        # Obtener las principales áreas de interés (top 3)
        sorted_areas = sorted(test_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        top_areas = [area for area, score in sorted_areas]
        
        # Para cada carrera, calcular compatibilidad basada en áreas
        for _, career_row in career_data.iterrows():
            career_id = int(career_row['id'])
            
            compatibility = 0.0
            
            # Comparar áreas de interés del estudiante con áreas de la carrera
            for area in top_areas:
                area_weight = career_row[f'area_{area}']
                compatibility += area_weight * test_scores[area]
            
            # Normalizar compatibilidad (0-1)
            compatibility = min(compatibility / 3.0, 1.0)
            
            results.append((career_id, float(compatibility)))
        
        # Ordenar por compatibilidad (descendente)
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results
    
    def save_model(self, model_path):
        """Guarda el modelo entrenado en un archivo"""
        if self.model is not None:
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler
            }, model_path)
            print(f"Modelo guardado en {model_path}")
    
    def load_model(self, model_path):
        """Carga un modelo previamente guardado"""
        if os.path.exists(model_path):
            data = joblib.load(model_path)
            self.model = data['model']
            self.scaler = data['scaler']
            print(f"Modelo cargado desde {model_path}")