import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import json

class DataPreprocessor:
    """
    Clase para preparar y procesar datos para alimentar los modelos de Machine Learning
    """
    
    def __init__(self):
        """Inicializa el preprocesador de datos"""
        self.scaler = StandardScaler()
    
    def process_test_answers(self, answers_json):
        """
        Procesa las respuestas del test CHASIDE en formato JSON
        
        Args:
            answers_json: String con las respuestas en formato JSON
            
        Returns:
            dict: Diccionario con puntajes por área
        """
        if not answers_json:
            return {
                'C': 0, 'H': 0, 'A': 0, 'S': 0,
                'I': 0, 'D': 0, 'E': 0
            }
        
        # Parsear JSON
        answers = json.loads(answers_json)
        
        # Mapeo de preguntas a áreas para intereses
        interest_map = {
            '1': 'C', '9': 'H', '3': 'A', '8': 'S', '6': 'I', '5': 'D', '17': 'E',
            '12': 'C', '25': 'H', '11': 'A', '16': 'S', '19': 'I', '14': 'D', '32': 'E',
            '20': 'C', '34': 'H', '21': 'A', '23': 'S', '27': 'I', '24': 'D', '35': 'E',
            '53': 'C', '41': 'H', '28': 'A', '33': 'S', '38': 'I', '31': 'D', '42': 'E',
            '64': 'C', '56': 'H', '36': 'A', '44': 'S', '47': 'I', '37': 'D', '49': 'E',
            '71': 'C', '67': 'H', '45': 'A', '52': 'S', '54': 'I', '48': 'D', '61': 'E',
            '78': 'C', '74': 'H', '50': 'A', '62': 'S', '60': 'I', '58': 'D', '68': 'E',
            '85': 'C', '80': 'H', '57': 'A', '70': 'S', '75': 'I', '65': 'D', '77': 'E',
            '91': 'C', '89': 'H', '81': 'A', '87': 'S', '83': 'I', '73': 'D', '88': 'E',
            '98': 'C', '95': 'H', '96': 'A', '92': 'S', '97': 'I', '84': 'D', '93': 'E'
        }
        
        # Mapeo de preguntas a áreas para aptitudes
        aptitude_map = {
            '2': 'C', '30': 'H', '22': 'A', '4': 'S', '10': 'I', '13': 'D', '7': 'E',
            '15': 'C', '63': 'H', '39': 'A', '29': 'S', '26': 'I', '18': 'D', '55': 'E',
            '46': 'C', '72': 'H', '76': 'A', '40': 'S', '59': 'I', '43': 'D', '79': 'E',
            '51': 'C', '86': 'H', '82': 'A', '69': 'S', '90': 'I', '66': 'D', '94': 'E'
        }
        
        # Inicializar contadores
        area_counts = {
            'C': 0, 'H': 0, 'A': 0, 'S': 0,
            'I': 0, 'D': 0, 'E': 0
        }
        
        # Contar respuestas positivas por área
        for question_id, is_yes in answers.items():
            if not is_yes:  # Solo considerar respuestas "Sí"
                continue
                
            # Verificar si es pregunta de interés
            if question_id in interest_map:
                area = interest_map[question_id]
                area_counts[area] += 1
            
            # Verificar si es pregunta de aptitud
            elif question_id in aptitude_map:
                area = aptitude_map[question_id]
                area_counts[area] += 1
        
        return area_counts
    
    def normalize_academic_scores(self, scores):
        """
        Normaliza las puntuaciones académicas a una escala estándar
        
        Args:
            scores: Diccionario con puntuaciones académicas
            
        Returns:
            dict: Puntuaciones normalizadas
        """
        # Convertir a DataFrame para usar StandardScaler
        df = pd.DataFrame([scores])
        
        # Aplicar normalización
        normalized = self.scaler.fit_transform(df)
        
        # Convertir de nuevo a diccionario
        norm_scores = {}
        for i, col in enumerate(df.columns):
            norm_scores[col] = normalized[0, i]
        
        return norm_scores
    
    def prepare_student_features(self, student, test_answers):
        """
        Prepara todas las características de un estudiante para los modelos
        
        Args:
            student: Objeto Student
            test_answers: Objeto TestAnswer
            
        Returns:
            pandas.DataFrame: Características procesadas
        """
        # Extraer notas académicas
        academic_scores = {
            'math_score': student.math_score if student.math_score is not None else 5.0,
            'science_score': student.science_score if student.science_score is not None else 5.0,
            'language_score': student.language_score if student.language_score is not None else 5.0,
            'social_science_score': student.social_science_score if student.social_science_score is not None else 5.0,
            'arts_score': student.arts_score if student.arts_score is not None else 5.0
        }
        
        # Extraer puntajes CHASIDE
        chaside_scores = {
            'score_c': test_answers.score_c,
            'score_h': test_answers.score_h,
            'score_a': test_answers.score_a,
            'score_s': test_answers.score_s,
            'score_i': test_answers.score_i,
            'score_d': test_answers.score_d,
            'score_e': test_answers.score_e
        }
        
        # Combinar todas las características
        features = {**academic_scores, **chaside_scores}
        
        # Convertir a DataFrame
        df = pd.DataFrame([features])
        
        return df