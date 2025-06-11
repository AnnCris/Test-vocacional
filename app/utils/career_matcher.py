# CREAR ARCHIVO NUEVO: app/utils/career_matcher.py

import numpy as np
import pandas as pd
import json
import os
from app.models.career import Career
from app.models.recommendation import Recommendation
from app import db

class CareerMatcher:
    """
    Sistema de recomendación MEJORADO que integra ML con reglas inteligentes
    """
    
    def __init__(self):
        """Inicializa el sistema"""
        self.models_loaded = False
        
        # Intentar cargar modelos ML si existen
        try:
            from app.ml_models.ensemble import EnsembleRecommender
            from app.ml_models.data_processor import DataProcessor
            
            self.recommender = EnsembleRecommender()
            self.data_processor = DataProcessor()
            
            # Buscar modelos guardados
            models_path = os.path.join('app', 'ml_models', 'saved_models')
            if os.path.exists(models_path) and os.listdir(models_path):
                try:
                    self.recommender.load_models(models_path)
                    self.models_loaded = True
                    print("✅ Modelos ML cargados - Usando IA avanzada")
                except:
                    print("⚠️ Modelos no disponibles - Usando reglas mejoradas")
            else:
                print("💡 Modelos no encontrados - Usando reglas mejoradas")
                
        except ImportError:
            print("📋 ML no disponible - Usando reglas mejoradas")
    
    def generate_recommendations(self, student, test_answers, top_n=5):
        """
        Genera recomendaciones MEJORADAS (ML + reglas inteligentes)
        """
        try:
            print(f"🎯 Generando {top_n} recomendaciones para {student.first_name}...")
            
            # Obtener todas las carreras
            all_careers = Career.query.all()
            if len(all_careers) == 0:
                print("⚠️ No hay carreras en la base de datos")
                return []
            
            # USAR ML SI ESTÁ DISPONIBLE
            if self.models_loaded:
                try:
                    recommendations = self._generate_ml_recommendations(
                        student, test_answers, all_careers, top_n
                    )
                    if recommendations:
                        print("🤖 Recomendaciones generadas con ML")
                        return recommendations
                except Exception as e:
                    print(f"⚠️ Error en ML: {e}")
            
            # USAR REGLAS MEJORADAS COMO RESPALDO
            print("📋 Usando reglas mejoradas...")
            return self._generate_improved_rules_recommendations(
                student, test_answers, all_careers, top_n
            )
            
        except Exception as e:
            print(f"❌ Error en CareerMatcher: {e}")
            return []
    
    def _generate_ml_recommendations(self, student, test_answers, careers, top_n):
        """Genera recomendaciones usando ML"""
        try:
            # Preparar datos del estudiante
            student_data = self.data_processor.prepare_student_data(student, test_answers)
            
            # Preparar datos de carreras
            career_data = self.data_processor.prepare_career_data(careers)
            
            # Generar recomendaciones con ensemble
            ml_recommendations = self.recommender.recommend_careers(
                student_data, career_data, top_n=top_n
            )
            
            # Convertir a objetos Recommendation
            result = []
            for rank, (career_id, score, main_model) in enumerate(ml_recommendations, 1):
                career = Career.query.get(career_id)
                if not career:
                    continue
                
                # Generar explicación
                explanation = self._generate_ml_explanation(
                    student, test_answers, career, score, main_model
                )
                
                recommendation = Recommendation(
                    student_id=student.id,
                    career_id=career.id,
                    score=score,
                    rank=rank,
                    explanation=json.dumps(explanation),
                    model_used=f'ml_{main_model}'
                )
                
                result.append(recommendation)
            
            return result
            
        except Exception as e:
            print(f"Error en ML: {e}")
            return []
    
    def _generate_improved_rules_recommendations(self, student, test_answers, careers, top_n):
        """Genera recomendaciones con reglas MEJORADAS"""
        try:
            # Extraer puntajes CHASIDE
            chaside_scores = {
                'c': test_answers.score_c,
                'h': test_answers.score_h,
                'a': test_answers.score_a,
                's': test_answers.score_s,
                'i': test_answers.score_i,
                'd': test_answers.score_d,
                'e': test_answers.score_e
            }
            
            # Encontrar áreas más fuertes del estudiante
            top_areas = sorted(chaside_scores.items(), key=lambda x: x[1], reverse=True)[:3]
            
            # Datos académicos del estudiante
            academic_areas = student.get_average_by_area()
            overall_academic = np.mean(list(academic_areas.values())) if academic_areas else 51
            
            # Calcular compatibilidad con cada carrera
            career_scores = []
            
            for career in careers:
                # Compatibilidad CHASIDE
                chaside_compatibility = 0.0
                total_weight = 0.0
                
                for area, score in top_areas:
                    area_weight = getattr(career, f'area_{area}', 0.0) or 0.0
                    if area_weight > 0:
                        chaside_compatibility += score * area_weight
                        total_weight += area_weight
                
                if total_weight > 0:
                    chaside_compatibility /= total_weight
                    chaside_compatibility = min(chaside_compatibility / 14.0, 1.0)  # Normalizar
                
                # 🇧🇴 BONUS ACADÉMICO BOLIVIANO
                academic_bonus = self._calculate_academic_bonus(
                    overall_academic, career, top_areas[0][0] if top_areas else 'c'
                )
                
                # BONUS POR CONSISTENCIA CHASIDE
                consistency_bonus = self._calculate_consistency_bonus(chaside_scores)
                
                # Puntuación final
                final_score = min(
                    chaside_compatibility + academic_bonus + consistency_bonus,
                    1.0
                )
                
                career_scores.append((career, final_score))
            
            # Ordenar por puntuación y tomar top N
            career_scores.sort(key=lambda x: x[1], reverse=True)
            top_careers = career_scores[:top_n]
            
            # Crear objetos Recommendation
            result = []
            for rank, (career, score) in enumerate(top_careers, 1):
                explanation = self._generate_rules_explanation(
                    student, test_answers, career, score, overall_academic
                )
                
                recommendation = Recommendation(
                    student_id=student.id,
                    career_id=career.id,
                    score=score,
                    rank=rank,
                    explanation=json.dumps(explanation),
                    model_used='reglas_mejoradas'
                )
                
                result.append(recommendation)
            
            return result
            
        except Exception as e:
            print(f"Error en reglas: {e}")
            return []
    
    def _calculate_academic_bonus(self, overall_academic, career, dominant_area):
        """Calcula bonus académico según sistema boliviano"""
        # Bonus base por rendimiento general
        if overall_academic >= 85:
            base_bonus = 0.15  # Excelente
        elif overall_academic >= 75:
            base_bonus = 0.10  # Muy bueno
        elif overall_academic >= 65:
            base_bonus = 0.05  # Bueno
        else:
            base_bonus = 0.0   # Regular
        
        # Bonus específico por área
        area_bonus = 0.0
        career_name = career.name.lower()
        
        if dominant_area == 'i' and any(word in career_name for word in ['ingenieria', 'sistemas', 'industrial']):
            area_bonus = 0.05
        elif dominant_area == 's' and any(word in career_name for word in ['medicina', 'enfermeria', 'salud']):
            area_bonus = 0.05
        elif dominant_area == 'c' and any(word in career_name for word in ['administracion', 'contabilidad', 'economia']):
            area_bonus = 0.05
        elif dominant_area == 'h' and any(word in career_name for word in ['psicologia', 'derecho', 'comunicacion']):
            area_bonus = 0.05
        
        return base_bonus + area_bonus
    
    def _calculate_consistency_bonus(self, chaside_scores):
        """Calcula bonus por consistencia en respuestas CHASIDE"""
        scores_list = list(chaside_scores.values())
        variance = np.var(scores_list)
        
        # Menor varianza = mayor consistencia = bonus
        if variance <= 2:
            return 0.05  # Muy consistente
        elif variance <= 4:
            return 0.03  # Consistente
        else:
            return 0.0   # Inconsistente
    
    def _generate_rules_explanation(self, student, test_answers, career, score, overall_academic):
        """Genera explicación para recomendación basada en reglas"""
        try:
            # Identificar área dominante
            chaside_scores = {
                'C': test_answers.score_c, 'H': test_answers.score_h,
                'A': test_answers.score_a, 'S': test_answers.score_s,
                'I': test_answers.score_i, 'D': test_answers.score_d,
                'E': test_answers.score_e
            }
            
            dominant_area = max(chaside_scores, key=chaside_scores.get)
            dominant_score = chaside_scores[dominant_area]
            
            # Mapeo de áreas
            area_names = {
                'C': 'Administrativas y Contables',
                'H': 'Humanísticas y Sociales',
                'A': 'Artísticas',
                'S': 'Ciencias de la Salud',
                'I': 'Ingeniería y Tecnología',
                'D': 'Defensa y Seguridad',
                'E': 'Ciencias Exactas'
            }
            
            # Generar explicación personalizada
            explanation_text = f"Tu perfil muestra una fuerte inclinación hacia {area_names.get(dominant_area, 'áreas técnicas')} "
            explanation_text += f"con {dominant_score}/14 puntos en el test CHASIDE. "
            
            if overall_academic >= 75:
                explanation_text += f"Tu excelente rendimiento académico ({overall_academic:.1f}/100) "
                explanation_text += f"te prepara muy bien para los desafíos de {career.name}."
            elif overall_academic >= 65:
                explanation_text += f"Tu buen rendimiento académico ({overall_academic:.1f}/100) "
                explanation_text += f"es adecuado para tener éxito en {career.name}."
            else:
                explanation_text += f"Con dedicación adicional en tus estudios "
                explanation_text += f"puedes tener éxito en {career.name}."
            
            return {
                "career_name": career.name,
                "faculty_name": career.faculty.name if career.faculty else "No especificada",
                "compatibility_score": round(score * 100, 1),
                "dominant_area": area_names.get(dominant_area, dominant_area),
                "dominant_score": dominant_score,
                "academic_performance": round(overall_academic, 1),
                "main_explanation": explanation_text,
                "system_used": "reglas_mejoradas_chaside",
                "areas_fortaleza": [
                    area for area, score in chaside_scores.items() 
                    if score >= 8
                ]
            }
            
        except Exception as e:
            print(f"Error generando explicación: {e}")
            return {"error": "No se pudo generar explicación"}
    
    def _generate_ml_explanation(self, student, test_answers, career, score, main_model):
        """Genera explicación para recomendación ML"""
        try:
            # Versión simplificada para ML
            academic_areas = student.get_average_by_area()
            overall_academic = np.mean(list(academic_areas.values())) if academic_areas else 51
            
            return {
                "career_name": career.name,
                "faculty_name": career.faculty.name if career.faculty else "No especificada",
                "compatibility_score": round(score * 100, 1),
                "main_model": main_model,
                "academic_performance": round(overall_academic, 1),
                "main_explanation": f"Basado en análisis con Inteligencia Artificial ({main_model}), "
                                  f"tu perfil muestra {score*100:.1f}% de compatibilidad con {career.name}. "
                                  f"El sistema consideró tu rendimiento académico y perfil vocacional completo.",
                "system_used": f"machine_learning_{main_model}"
            }
            
        except Exception as e:
            print(f"Error en explicación ML: {e}")
            return {"error": "No se pudo generar explicación ML"}