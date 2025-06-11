# REEMPLAZA COMPLETAMENTE: app/utils/career_matcher.py

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
        
        # Verificar si hay estado de entrenamiento
        models_path = os.path.join('app', 'ml_models', 'saved_models')
        status_file = os.path.join(models_path, 'training_status.json')
        
        if os.path.exists(status_file):
            try:
                with open(status_file, 'r') as f:
                    status = json.load(f)
                    if status.get('trained', False):
                        self.models_loaded = True
                        print("✅ Modelos ML disponibles - Usando IA avanzada")
                    else:
                        print("📋 Usando reglas mejoradas")
            except:
                print("📋 Usando reglas mejoradas")
        else:
            print("💡 Modelos no encontrados - Usando reglas mejoradas")
    
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
            # Intentar cargar modelos individuales
            from app.ml_models.logistic_regression import CareerLogisticRegression
            from app.ml_models.decision_tree import CareerDecisionTree
            from app.ml_models.knn import CareerKNN
            
            models_path = os.path.join('app', 'ml_models', 'saved_models')
            
            # Preparar datos del estudiante
            student_data = self._prepare_student_features(student, test_answers)
            career_data = self._prepare_career_data(careers)
            
            # Cargar modelos disponibles
            models = {}
            
            # Regresión Logística
            try:
                logistic_model = CareerLogisticRegression(
                    os.path.join(models_path, 'logistic_model.pkl')
                )
                models['logistic'] = logistic_model
            except:
                pass
            
            # Árbol de Decisión
            try:
                tree_model = CareerDecisionTree(
                    os.path.join(models_path, 'tree_model.pkl')
                )
                models['tree'] = tree_model
            except:
                pass
            
            # KNN
            try:
                knn_model = CareerKNN(
                    model_path=os.path.join(models_path, 'knn_model.pkl')
                )
                models['knn'] = knn_model
            except:
                pass
            
            if not models:
                print("⚠️ No se pudieron cargar modelos ML")
                return []
            
            # Generar predicciones con modelos disponibles
            all_predictions = {}
            
            for model_name, model in models.items():
                try:
                    if model_name == 'logistic':
                        predictions = model.predict_compatibility(student_data, career_data)
                    elif model_name == 'tree':
                        predictions = model.predict_best_careers(student_data, career_data, top_n=10)
                    elif model_name == 'knn':
                        predictions = model.predict_career_compatibility(student_data, career_data)
                    
                    all_predictions[model_name] = predictions
                except Exception as e:
                    print(f"⚠️ Error con modelo {model_name}: {e}")
                    continue
            
            if not all_predictions:
                return []
            
            # Combinar predicciones
            combined_scores = {}
            model_weights = {name: 1.0/len(all_predictions) for name in all_predictions}
            
            for model_name, predictions in all_predictions.items():
                weight = model_weights[model_name]
                for career_id, score in predictions[:top_n*2]:  # Considerar más carreras
                    if career_id in combined_scores:
                        combined_scores[career_id] += score * weight
                    else:
                        combined_scores[career_id] = score * weight
            
            # Ordenar y tomar top N
            sorted_careers = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
            top_careers = sorted_careers[:top_n]
            
            # Convertir a objetos Recommendation
            result = []
            for rank, (career_id, score) in enumerate(top_careers, 1):
                career = db.session.get(Career, career_id)  # CORREGIDO: Usar db.session.get
                if not career:
                    continue
                
                # Generar explicación
                explanation = self._generate_ml_explanation(
                    student, test_answers, career, score, 'ensemble'
                )
                
                recommendation = Recommendation(
                    student_id=student.id,
                    career_id=career.id,
                    score=score,
                    rank=rank,
                    explanation=json.dumps(explanation),
                    model_used='ml_ensemble'
                )
                
                result.append(recommendation)
            
            return result
            
        except Exception as e:
            print(f"Error en ML: {e}")
            return []
    
    def _prepare_student_features(self, student, test_answers):
        """Prepara características del estudiante para ML"""
        # Datos académicos por área (sistema boliviano)
        areas_averages = student.get_average_by_area()
        
        # Datos del estudiante con MEJORAS
        student_data = {
            # Promedios académicos normalizados (0-1)
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
            
            # Características adicionales
            'dominant_chaside_area': self._get_dominant_area(test_answers),
            'academic_performance_level': self._get_academic_level(areas_averages),
            'chaside_consistency': self._calculate_chaside_consistency(test_answers)
        }
        
        return pd.DataFrame([student_data])
    
    def _prepare_career_data(self, careers):
        """Prepara datos de carreras"""
        career_data = []
        
        for career in careers:
            data = {
                'id': career.id,
                'faculty_id': career.faculty_id,
                'area_c': career.area_c or 0.0,
                'area_h': career.area_h or 0.0,
                'area_a': career.area_a or 0.0,
                'area_s': career.area_s or 0.0,
                'area_i': career.area_i or 0.0,
                'area_d': career.area_d or 0.0,
                'area_e': career.area_e or 0.0
            }
            career_data.append(data)
        
        return pd.DataFrame(career_data)
    
    def _get_dominant_area(self, test_answers):
        """Identifica el área CHASIDE dominante"""
        scores = {
            'C': test_answers.score_c, 'H': test_answers.score_h,
            'A': test_answers.score_a, 'S': test_answers.score_s,
            'I': test_answers.score_i, 'D': test_answers.score_d,
            'E': test_answers.score_e
        }
        dominant = max(scores, key=scores.get)
        area_mapping = {'C': 0, 'H': 1, 'A': 2, 'S': 3, 'I': 4, 'D': 5, 'E': 6}
        return area_mapping.get(dominant, 0)
    
    def _get_academic_level(self, areas_averages):
        """Determina nivel académico"""
        overall_avg = np.mean(list(areas_averages.values())) if areas_averages else 51
        if overall_avg >= 80:
            return 2  # Alto
        elif overall_avg >= 65:
            return 1  # Medio
        else:
            return 0  # Bajo
    
    def _calculate_chaside_consistency(self, test_answers):
        """Calcula consistencia CHASIDE"""
        scores = [
            test_answers.score_c, test_answers.score_h, test_answers.score_a,
            test_answers.score_s, test_answers.score_i, test_answers.score_d,
            test_answers.score_e
        ]
        variance = np.var(scores)
        max_variance = np.var([14, 0, 0, 0, 0, 0, 0])
        return 1 - (variance / max_variance) if max_variance > 0 else 1
    
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