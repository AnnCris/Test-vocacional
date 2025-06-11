import numpy as np
import pandas as pd
import json
from app.ml_models.ensemble import EnsembleRecommender
from app.models.career import Career
from app.models.recommendation import Recommendation
from app import db

class CareerMatcher:
    """
    Clase encargada de generar recomendaciones de carreras para los estudiantes
    basándose en los resultados del test CHASIDE y los modelos de ML
    """
    
    def __init__(self):
        """Inicializa el sistema de recomendación"""
        self.recommender = EnsembleRecommender()
        self.models_path = 'app/ml_models/saved_models'
        
        # Intentar cargar modelos pre-entrenados
        try:
            self.recommender.load_models(self.models_path)
            self.models_loaded = True
        except:
            self.models_loaded = False
    
    def generate_recommendations(self, student, test_answers):
        """
        Genera recomendaciones de carreras para un estudiante
        
        Args:
            student: Objeto Student con información del estudiante
            test_answers: Objeto TestAnswer con respuestas del test
            
        Returns:
            list: Lista de objetos Recommendation
        """
        # Preparar datos del estudiante
        student_data = self._prepare_student_data(student, test_answers)
        
        # Obtener todas las carreras
        all_careers = Career.query.all()
        career_data = self._prepare_career_data(all_careers)
        
        # Generar recomendaciones (top 5)
        if self.models_loaded:
            # Usar ensemble de modelos
            recommendations = self.recommender.recommend_careers(student_data, career_data, top_n=5)
            model_used = 'ensemble'
        else:
            # Usar enfoque basado en reglas si no hay modelos entrenados
            recommendations = self._rule_based_recommendations(student_data, career_data, top_n=5)
            model_used = 'rule_based'
        
        # Crear objetos de recomendación para la base de datos
        result = []
        
        for rank, (career_id, score, _) in enumerate(recommendations, 1):
            career = Career.query.get(career_id)
            if not career:
                continue
                
            # Generar explicación
            explanation = self._generate_explanation(student, test_answers, career, score)
            
            # Crear objeto de recomendación
            recommendation = Recommendation(
                student_id=student.id,
                career_id=career.id,
                score=score,
                rank=rank,
                explanation=json.dumps(explanation),
                model_used=model_used
            )
            
            result.append(recommendation)
            
        return result
    
    def _prepare_student_data(self, student, test_answers):
        """Prepara los datos del estudiante para los modelos"""
        data = {
            'math_score': [student.math_score if student.math_score is not None else 5.0],
            'science_score': [student.science_score if student.science_score is not None else 5.0],
            'language_score': [student.language_score if student.language_score is not None else 5.0],
            'social_science_score': [student.social_science_score if student.social_science_score is not None else 5.0],
            'arts_score': [student.arts_score if student.arts_score is not None else 5.0],
            'score_c': [test_answers.score_c],
            'score_h': [test_answers.score_h],
            'score_a': [test_answers.score_a],
            'score_s': [test_answers.score_s],
            'score_i': [test_answers.score_i],
            'score_d': [test_answers.score_d],
            'score_e': [test_answers.score_e]
        }
        
        return pd.DataFrame(data)
    
    def _prepare_career_data(self, careers):
        """Prepara los datos de las carreras para los modelos"""
        data = []
        
        for career in careers:
            career_data = {
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
            data.append(career_data)
        
        return pd.DataFrame(data)
    
    def _rule_based_recommendations(self, student_data, career_data, top_n=5):
        """
        Genera recomendaciones basadas en reglas cuando no hay modelos entrenados
        
        Args:
            student_data: DataFrame con datos del estudiante
            career_data: DataFrame con datos de las carreras
            top_n: Número de recomendaciones a generar
            
        Returns:
            list: Lista de tuplas (id_carrera, puntuación, modelo)
        """
        results = []
        
        # Extraer puntajes CHASIDE
        chaside_scores = {
            'c': student_data['score_c'].values[0],
            'h': student_data['score_h'].values[0],
            'a': student_data['score_a'].values[0],
            's': student_data['score_s'].values[0],
            'i': student_data['score_i'].values[0],
            'd': student_data['score_d'].values[0],
            'e': student_data['score_e'].values[0]
        }
        
        # Obtener las 3 áreas con mayor puntaje
        top_areas = sorted(chaside_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Calcular compatibilidad con cada carrera
        for _, career in career_data.iterrows():
            career_id = int(career['id'])
            compatibility = 0.0
            
            # Para cada área top, calcular compatibilidad
            for area, score in top_areas:
                area_weight = career[f'area_{area}']
                compatibility += area_weight * score
            
            # Normalizar (0-1)
            max_possible = sum(score for _, score in top_areas)
            if max_possible > 0:
                compatibility /= max_possible
            
            # Considerar notas académicas
            academic_weights = {
                'c': ['math_score', 'social_science_score'],  # Administrativas
                'h': ['language_score', 'social_science_score'],  # Humanísticas
                'a': ['arts_score'],  # Artísticas
                's': ['science_score', 'math_score'],  # Salud
                'i': ['math_score', 'science_score'],  # Ingeniería
                'd': ['social_science_score', 'math_score'],  # Defensa
                'e': ['science_score', 'math_score']  # Ciencias exactas
            }
            
            academic_score = 0.0
            count = 0
            
            for area, _ in top_areas:
                for subject in academic_weights.get(area, []):
                    if subject in student_data:
                        academic_score += student_data[subject].values[0] / 10.0  # Normalizar a 0-1
                        count += 1
            
            if count > 0:
                academic_score /= count
                
                # Ajustar compatibilidad considerando notas (70% test, 30% notas)
                compatibility = 0.7 * compatibility + 0.3 * academic_score
            
            results.append((career_id, float(compatibility), 'rule_based'))
        
        # Ordenar por compatibilidad
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:top_n]
    
    def _generate_explanation(self, student, test_answers, career, score):
        """
        Genera una explicación detallada para la recomendación
        
        Args:
            student: Objeto Student
            test_answers: Objeto TestAnswer
            career: Objeto Career
            score: Puntuación de compatibilidad
            
        Returns:
            dict: Explicación detallada
        """
        # Extraer áreas CHASIDE más relevantes para esta carrera
        career_areas = {
            'C': ('Administrativas y contables', career.area_c),
            'H': ('Humanísticas y sociales', career.area_h),
            'A': ('Artísticas', career.area_a),
            'S': ('Ciencias de la salud', career.area_s),
            'I': ('Ingeniería y computación', career.area_i),
            'D': ('Defensa y seguridad', career.area_d),
            'E': ('Ciencias exactas y naturales', career.area_e)
        }
        
        # Ordenar áreas por relevancia para esta carrera
        sorted_areas = sorted(career_areas.items(), key=lambda x: x[1][1], reverse=True)
        
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
        
        # Identificar áreas de coincidencia
        matched_areas = []
        
        for area_code, (area_name, importance) in sorted_areas[:3]:
            if importance >= 0.4:  # Solo considerar áreas relevantes
                student_score = student_scores[area_code]
                # Convertir de 0-10 a 0-100%
                match_percentage = min(student_score * 10, 100)
                
                if match_percentage >= 50:  # Coincidencia significativa
                    matched_areas.append({
                        'area_code': area_code,
                        'area_name': area_name,
                        'importance_for_career': round(importance * 100),  # Convertir a porcentaje
                        'student_score': student_score,
                        'match_percentage': round(match_percentage)
                    })
        
        # Calcular puntuación académica según áreas relevantes
      # Calcular puntuación académica según áreas relevantes
        academic_relevance = {
            'C': {'math_score': 0.7, 'language_score': 0.3, 'social_science_score': 0.5},
            'H': {'language_score': 0.8, 'social_science_score': 0.7, 'arts_score': 0.4},
            'A': {'arts_score': 0.9, 'language_score': 0.5, 'social_science_score': 0.3},
            'S': {'science_score': 0.8, 'math_score': 0.6, 'social_science_score': 0.4},
            'I': {'math_score': 0.9, 'science_score': 0.7, 'language_score': 0.2},
            'D': {'social_science_score': 0.7, 'math_score': 0.5, 'science_score': 0.3},
            'E': {'science_score': 0.9, 'math_score': 0.8, 'social_science_score': 0.2}
        }
        
        relevant_subjects = []
        
        # Para las 2 áreas más importantes de la carrera
        for area_code, (area_name, importance) in sorted_areas[:2]:
            if importance >= 0.5:  # Solo áreas muy relevantes
                subjects = academic_relevance.get(area_code, {})
                
                for subject, rel in subjects.items():
                    if rel >= 0.5:  # Solo materias relevantes
                        attr_name = subject
                        score = getattr(student, attr_name, None)
                        
                        if score is not None:
                            subject_names = {
                                'math_score': 'Matemáticas',
                                'science_score': 'Ciencias',
                                'language_score': 'Lenguaje',
                                'social_science_score': 'Ciencias Sociales',
                                'arts_score': 'Arte'
                            }
                            
                            subject_name = subject_names.get(subject, subject)
                            
                            relevant_subjects.append({
                                'subject': subject_name,
                                'score': score,
                                'relevance': round(rel * 100)  # Convertir a porcentaje
                            })
        
        # Generar la explicación completa
        explanation = {
            'career_name': career.name,
            'faculty_name': career.faculty.name,
            'compatibility_score': round(score * 100),  # Convertir a porcentaje
            'matched_areas': matched_areas,
            'academic_subjects': relevant_subjects,
            'recommendation_reason': self._generate_recommendation_reason(
                career, matched_areas, relevant_subjects
            ),
            'career_description': career.description
        }
        
        return explanation
    
    def _generate_recommendation_reason(self, career, matched_areas, relevant_subjects):
        """
        Genera un texto explicativo de la recomendación
        
        Args:
            career: Objeto Career
            matched_areas: Lista de áreas coincidentes
            relevant_subjects: Lista de materias relevantes
            
        Returns:
            str: Texto explicativo
        """
        # Si no hay áreas coincidentes, dar una explicación general
        if not matched_areas:
            return f"La carrera de {career.name} podría ser una buena opción basada en tu perfil general."
        
        # Construir razón basada en áreas coincidentes
        main_area = matched_areas[0]
        
        reason = f"Según tus resultados en el test CHASIDE, muestras una fuerte inclinación hacia el área {main_area['area_name']} "
        reason += f"(coincidencia del {main_area['match_percentage']}%), que es fundamental para la carrera de {career.name}. "
        
        # Agregar información sobre materias relevantes si están disponibles
        if relevant_subjects:
            top_subject = relevant_subjects[0]
            
            if top_subject['score'] >= 7:  # Buena puntuación
                reason += f"Además, tu buen rendimiento en {top_subject['subject']} ({top_subject['score']}/10) "
                reason += f"es muy valioso para esta carrera, donde esta materia tiene una relevancia del {top_subject['relevance']}%."
            else:
                reason += f"Aunque tu desempeño en {top_subject['subject']} podría mejorar, esta área es relevante para la carrera "
                reason += f"con una importancia del {top_subject['relevance']}%."
        
        # Recomendación final
        if len(matched_areas) > 1:
            reason += f" También muestras aptitudes en el área {matched_areas[1]['area_name']}, que complementa bien tu perfil para esta carrera."
        
        return reason