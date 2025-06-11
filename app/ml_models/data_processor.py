import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import json

class DataProcessor:
    """
    Clase para preprocesar los datos antes de alimentar los modelos de ML
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
        
    def prepare_student_data(self, student, test_answers):
        """
        Prepara los datos de un estudiante para que sean utilizados por los modelos ML
        
        Args:
            student: Objeto Student de la base de datos
            test_answers: Objeto TestAnswer con las respuestas del test
            
        Returns:
            DataFrame: Datos del estudiante procesados
        """
        # Recopilar datos del estudiante
        student_data = {
            'math_score': student.math_score if student.math_score else 5.0,
            'science_score': student.science_score if student.science_score else 5.0,
            'language_score': student.language_score if student.language_score else 5.0,
            'social_science_score': student.social_science_score if student.social_science_score else 5.0,
            'arts_score': student.arts_score if student.arts_score else 5.0,
            'score_c': test_answers.score_c,
            'score_h': test_answers.score_h,
            'score_a': test_answers.score_a,
            'score_s': test_answers.score_s,
            'score_i': test_answers.score_i,
            'score_d': test_answers.score_d,
            'score_e': test_answers.score_e
        }
        
        # Convertir a DataFrame
        student_df = pd.DataFrame([student_data])
        
        # Normalizar datos numéricos
        numerical_cols = ['math_score', 'science_score', 'language_score', 
                         'social_science_score', 'arts_score',
                         'score_c', 'score_h', 'score_a', 'score_s', 
                         'score_i', 'score_d', 'score_e']
        
        student_df[numerical_cols] = self.scaler.fit_transform(student_df[numerical_cols])
        
        return student_df
    
    def prepare_career_data(self, careers):
        """
        Prepara los datos de las carreras para la predicción
        
        Args:
            careers: Lista de objetos Career de la base de datos
            
        Returns:
            DataFrame: Datos de carreras procesados
        """
        career_data = []
        
        for career in careers:
            data = {
                'id': career.id,
                'faculty_id': career.faculty_id,
                'area_c': career.area_c,
                'area_h': career.area_h,
                'area_a': career.area_a,
                'area_s': career.area_s,
                'area_i': career.area_i,
                'area_d': career.area_d,
                'area_e': career.area_e
            }
            career_data.append(data)
        
        # Convertir a DataFrame
        career_df = pd.DataFrame(career_data)
        
        # Codificar facultad con one-hot encoding
        faculty_encoded = self.encoder.fit_transform(career_df[['faculty_id']])
        faculty_df = pd.DataFrame(
            faculty_encoded, 
            columns=[f'faculty_{i}' for i in range(faculty_encoded.shape[1])]
        )
        
        # Unir datos
        career_df = pd.concat([
            career_df.drop('faculty_id', axis=1),
            faculty_df
        ], axis=1)
        
        return career_df
    
    def get_detailed_responses(self, test_answers):
        """
        Extrae las respuestas detalladas del JSON almacenado
        
        Args:
            test_answers: Objeto TestAnswer con la respuesta del test
            
        Returns:
            dict: Respuestas detalladas por pregunta
        """
        if not test_answers.answers_json:
            return {}
        
        return json.loads(test_answers.answers_json)
    
    def get_feature_importance(self, student_data, model):
        """
        Calcula la importancia de las características si el modelo lo soporta
        
        Args:
            student_data: DataFrame con los datos del estudiante
            model: Modelo entrenado que tiene atributo feature_importances_
            
        Returns:
            dict: Diccionario con la importancia de cada característica
        """
        if not hasattr(model, 'feature_importances_'):
            return {}
        
        feature_importance = {}
        for feature, importance in zip(student_data.columns, model.feature_importances_):
            feature_importance[feature] = importance
        
        return feature_importance