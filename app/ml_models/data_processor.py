# REEMPLAZA COMPLETAMENTE: app/ml_models/data_processor.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import json

class DataProcessor:
    """
    Clase mejorada para el sistema boliviano con integración CHASIDE + ML
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        
    def prepare_student_data(self, student, test_answers):
        """
        Prepara datos del estudiante (SISTEMA BOLIVIANO mejorado)
        """
        # Calcular promedios por área según el sistema boliviano
        areas_averages = student.get_average_by_area()
        
        # Datos del estudiante con MEJORAS
        student_data = {
            # Promedios académicos (escala boliviana 1-100 → 0-1)
            'matematicas_exactas_avg': areas_averages.get('matematicas_exactas', 51) / 100.0,
            'ciencias_naturales_avg': areas_averages.get('ciencias_naturales', 51) / 100.0,
            'comunicacion_lenguaje_avg': areas_averages.get('comunicacion_lenguaje', 51) / 100.0,
            'ciencias_sociales_avg': areas_averages.get('ciencias_sociales', 51) / 100.0,
            'artes_expresion_avg': areas_averages.get('artes_expresion', 51) / 100.0,
            'educacion_fisica_avg': areas_averages.get('educacion_fisica', 51) / 100.0,
            
            # Puntajes CHASIDE normalizados
            'score_c': test_answers.score_c / 14.0,
            'score_h': test_answers.score_h / 14.0,
            'score_a': test_answers.score_a / 14.0,
            'score_s': test_answers.score_s / 14.0,
            'score_i': test_answers.score_i / 14.0,
            'score_d': test_answers.score_d / 14.0,
            'score_e': test_answers.score_e / 14.0,
            
            # NUEVAS CARACTERÍSTICAS INTELIGENTES
            'dominant_chaside_area': self._get_dominant_area(test_answers),
            'academic_performance_level': self._get_academic_level(areas_averages),
            'chaside_consistency': self._calculate_chaside_consistency(test_answers)
        }
        
        return pd.DataFrame([student_data])
    
    def _get_dominant_area(self, test_answers):
        """Identifica el área CHASIDE dominante (NUEVO)"""
        scores = {
            'C': test_answers.score_c, 'H': test_answers.score_h,
            'A': test_answers.score_a, 'S': test_answers.score_s,
            'I': test_answers.score_i, 'D': test_answers.score_d,
            'E': test_answers.score_e
        }
        dominant = max(scores, key=scores.get)
        # Convertir a valor numérico para ML
        area_mapping = {'C': 0, 'H': 1, 'A': 2, 'S': 3, 'I': 4, 'D': 5, 'E': 6}
        return area_mapping.get(dominant, 0)
    
    def _get_academic_level(self, areas_averages):
        """Determina nivel académico (NUEVO)"""
        overall_avg = np.mean(list(areas_averages.values()))
        if overall_avg >= 80:
            return 2  # Alto
        elif overall_avg >= 65:
            return 1  # Medio
        else:
            return 0  # Bajo
    
    def _calculate_chaside_consistency(self, test_answers):
        """Calcula consistencia CHASIDE (NUEVO)"""
        scores = [
            test_answers.score_c, test_answers.score_h, test_answers.score_a,
            test_answers.score_s, test_answers.score_i, test_answers.score_d,
            test_answers.score_e
        ]
        variance = np.var(scores)
        max_variance = np.var([14, 0, 0, 0, 0, 0, 0])
        return 1 - (variance / max_variance) if max_variance > 0 else 1
    
    def prepare_career_data(self, careers):
        """Prepara datos de carreras (MEJORADO)"""
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
        
        return pd.DataFrame(career_data)
    
    # Mantener métodos originales para compatibilidad
    def get_detailed_responses(self, test_answers):
        if not test_answers.answers_json:
            return {}
        try:
            return json.loads(test_answers.answers_json)
        except json.JSONDecodeError:
            return {}
    
    def get_feature_importance(self, student_data, model):
        if not hasattr(model, 'feature_importances_'):
            return {}
        
        feature_importance = {}
        for feature, importance in zip(student_data.columns, model.feature_importances_):
            feature_importance[feature] = importance
        
        return feature_importance