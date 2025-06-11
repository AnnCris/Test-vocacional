# REEMPLAZA COMPLETAMENTE: train_models_improved.py

#!/usr/bin/env python3
"""
Script CORREGIDO para entrenar modelos ML
"""

import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime
import warnings

# Silenciar advertencias molestas
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

def main():
    print("🤖 Entrenamiento de Modelos ML - Sistema de Recomendación")
    print("=" * 60)
    
    try:
        # Importar la aplicación
        from app import create_app, db
        from app.models.student import Student
        from app.models.test_answer import TestAnswer
        from app.models.recommendation import Recommendation  # CORREGIDO: Importación agregada
        from app.models.career import Career
        
        app = create_app()
        
        with app.app_context():
            # Verificar datos existentes
            students_count = Student.query.count()
            tests_count = TestAnswer.query.count()
            careers_count = Career.query.count()
            recommendations_count = Recommendation.query.count()  # CORREGIDO: Agregado
            
            print(f"📊 Datos actuales:")
            print(f"   - Estudiantes: {students_count}")
            print(f"   - Tests: {tests_count}")
            print(f"   - Carreras: {careers_count}")
            print(f"   - Recomendaciones: {recommendations_count}")  # CORREGIDO: Agregado
            
            if careers_count == 0:
                print("❌ Error: No hay carreras en la base de datos")
                print("💡 Ejecuta primero: python init_db.py")
                return False
            
            # Intentar entrenar modelos
            if recommendations_count >= 5:  # CORREGIDO: Usar recomendaciones en lugar de tests
                print("\n🎯 Intentando entrenar con datos reales...")
                success = train_with_real_data(app)
                if success:
                    print("✅ ¡Modelos entrenados con datos reales!")
                    return True
                else:
                    print("⚠️ Error con datos reales, usando sintéticos...")
            else:
                print(f"\n💡 Necesitas al menos 5 recomendaciones para entrenar (tienes {recommendations_count})")
            
            # Entrenar con datos sintéticos
            print("\n🔄 Generando datos sintéticos para entrenamiento...")
            success = train_with_synthetic_data(app)
            
            if success:
                print("✅ ¡Modelos entrenados con datos sintéticos!")
                print("💡 Los modelos mejorarán automáticamente con más datos reales")
                print("🚀 Ahora tu sistema usa Inteligencia Artificial!")
            else:
                print("⚠️ No se pudieron entrenar modelos ML")
                print("💡 El sistema funcionará con reglas mejoradas")
            
            return success
            
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Instala dependencias: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

def train_with_real_data(app):
    """Entrenar con datos reales de la base de datos - CORREGIDO"""
    try:
        from app.ml_models.ensemble import EnsembleRecommender
        from app.ml_models.data_processor import DataProcessor
        from app.models.student import Student  # CORREGIDO: Importación agregada
        from app.models.test_answer import TestAnswer  # CORREGIDO: Importación agregada
        from app.models.recommendation import Recommendation  # CORREGIDO: Importación agregada
        
        with app.app_context():
            # Recopilar datos reales - CORREGIDO
            recommendations = Recommendation.query.all()
            
            if len(recommendations) < 5:
                print("⚠️ Pocos datos reales para entrenamiento")
                return False
            
            # Preparar datos para entrenamiento
            training_data = []
            labels = []
            
            processor = DataProcessor()
            
            print(f"🔄 Procesando {len(recommendations)} recomendaciones...")
            
            for rec in recommendations:
                try:
                    student = Student.query.get(rec.student_id)
                    test_answer = TestAnswer.query.filter_by(student_id=student.id).first()
                    
                    if student and test_answer:
                        # Preparar características
                        student_features = processor.prepare_student_data(student, test_answer)
                        training_data.append(student_features.iloc[0].values)
                        labels.append(rec.career_id)
                except Exception as e:
                    print(f"⚠️ Error procesando recomendación {rec.id}: {e}")
                    continue
            
            if len(training_data) < 3:
                print("⚠️ No hay suficientes datos válidos")
                return False
            
            print(f"✅ {len(training_data)} muestras de entrenamiento preparadas")
            
            # Entrenar ensemble
            X = np.array(training_data)
            y = np.array(labels)
            
            ensemble = EnsembleRecommender()
            
            # CORREGIDO: Preparar student_profiles para KNN
            student_profiles = pd.DataFrame([
                {
                    'student_id': rec.student_id,
                    'career_id': rec.career_id,
                    'score': rec.score
                } for rec in recommendations
            ])
            
            success = ensemble.train_models(X, y, student_profiles)
            
            if success:
                # Guardar modelos
                models_dir = os.path.join('app', 'ml_models', 'saved_models')
                os.makedirs(models_dir, exist_ok=True)
                ensemble.save_models(models_dir)
                print(f"💾 Modelos guardados en: {models_dir}")
                return True
            
        return False
        
    except Exception as e:
        print(f"Error entrenando con datos reales: {e}")
        import traceback
        traceback.print_exc()
        return False

def train_with_synthetic_data(app):
    """Entrenar con datos sintéticos - MEJORADO"""
    try:
        from app.ml_models.ensemble import EnsembleRecommender
        from app.ml_models.data_processor import DataProcessor
        from app.models.career import Career
        
        with app.app_context():
            # Obtener carreras disponibles
            careers = Career.query.all()
            
            if len(careers) == 0:
                print("❌ No hay carreras disponibles")
                return False
            
            print(f"🔄 Generando datos sintéticos para {len(careers)} carreras...")
            
            # Generar datos sintéticos MEJORADOS
            synthetic_data = generate_improved_synthetic_students(careers, num_samples=100)  # CORREGIDO: Más muestras
            
            if len(synthetic_data) < 20:  # CORREGIDO: Mínimo más bajo
                print("❌ No se pudieron generar suficientes datos sintéticos")
                return False
            
            # Preparar para entrenamiento
            X = np.array([data['features'] for data in synthetic_data])
            y = np.array([data['career_id'] for data in synthetic_data])
            
            print(f"📊 Datos de entrenamiento: {X.shape[0]} muestras, {X.shape[1]} características")
            
            # CORREGIDO: Preparar student_profiles sintéticos para KNN
            student_profiles = pd.DataFrame([
                {
                    'student_id': 1000 + i,
                    'career_id': data['career_id'],
                    'student_type': data['student_type']
                } for i, data in enumerate(synthetic_data)
            ])
            
            # Entrenar ensemble
            ensemble = EnsembleRecommender()
            print("🧠 Entrenando algoritmos de Machine Learning...")
            
            try:
                success = ensemble.train_models(X, y, student_profiles)
                
                if success:
                    # Guardar modelos
                    models_dir = os.path.join('app', 'ml_models', 'saved_models')
                    os.makedirs(models_dir, exist_ok=True)
                    ensemble.save_models(models_dir)
                    
                    print(f"💾 Modelos guardados en: {models_dir}")
                    print("🎯 Precisión de modelos:")
                    for model, acc in ensemble.model_accuracies.items():
                        print(f"   - {model}: {acc:.2%}")
                    
                    return True
                else:
                    print("❌ Error en el entrenamiento del ensemble")
                    return False
                    
            except Exception as e:
                print(f"❌ Error entrenando ensemble: {e}")
                return False
            
    except Exception as e:
        print(f"Error entrenando con datos sintéticos: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_improved_synthetic_students(careers, num_samples=100):
    """Genera estudiantes sintéticos MEJORADOS"""
    synthetic_data = []
    
    # Tipos de estudiantes más variados
    student_types = [
        'matematico_fuerte', 'humanistico_puro', 'artistico_creativo', 
        'cientifico_investigador', 'equilibrado_versatil', 'tecnologico_innovador',
        'social_comunicativo', 'practico_aplicado'
    ]
    
    print(f"🎲 Generando {num_samples} perfiles de estudiantes variados...")
    
    for i in range(num_samples):
        try:
            # Elegir tipo de estudiante
            student_type = np.random.choice(student_types)
            
            # Generar perfil específico por tipo - MEJORADO
            academic_scores, chaside_scores = generate_student_profile(student_type)
            
            # Normalizar scores académicos (0-1)
            norm_academic = {k: v/100.0 for k, v in academic_scores.items()}
            norm_chaside = {k: v/14.0 for k, v in chaside_scores.items()}
            
            # Calcular características adicionales
            dominant_area = max(chaside_scores, key=chaside_scores.get)
            area_mapping = {'c': 0, 'h': 1, 'a': 2, 's': 3, 'i': 4, 'd': 5, 'e': 6}
            dominant_numeric = area_mapping.get(dominant_area, 0)
            
            academic_avg = np.mean(list(academic_scores.values()))
            academic_level = 2 if academic_avg >= 80 else 1 if academic_avg >= 65 else 0
            
            chaside_variance = np.var(list(chaside_scores.values()))
            max_variance = np.var([14, 0, 0, 0, 0, 0, 0])
            consistency = 1 - (chaside_variance / max_variance) if max_variance > 0 else 1
            
            # Crear vector de características
            features = [
                norm_academic['matematicas_exactas'],
                norm_academic['ciencias_naturales'],
                norm_academic['comunicacion_lenguaje'],
                norm_academic['ciencias_sociales'],
                norm_academic['artes_expresion'],
                norm_academic['educacion_fisica'],
                norm_chaside['c'], norm_chaside['h'], norm_chaside['a'],
                norm_chaside['s'], norm_chaside['i'], norm_chaside['d'], norm_chaside['e'],
                dominant_numeric,
                academic_level,
                consistency
            ]
            
            # Encontrar mejor carrera para este perfil
            best_career = find_best_career_for_profile_improved(chaside_scores, careers, academic_scores)
            
            if best_career:
                synthetic_data.append({
                    'features': features,
                    'career_id': best_career.id,
                    'student_type': student_type
                })
                
        except Exception as e:
            print(f"⚠️ Error generando muestra {i}: {e}")
            continue
    
    print(f"✅ Generadas {len(synthetic_data)} muestras sintéticas válidas")
    return synthetic_data

def generate_student_profile(student_type):
    """Genera perfil académico y CHASIDE según tipo de estudiante - MEJORADO"""
    
    if student_type == 'matematico_fuerte':
        academic_scores = {
            'matematicas_exactas': np.random.uniform(80, 95),
            'ciencias_naturales': np.random.uniform(70, 90),
            'comunicacion_lenguaje': np.random.uniform(55, 75),
            'ciencias_sociales': np.random.uniform(60, 80),
            'artes_expresion': np.random.uniform(50, 70),
            'educacion_fisica': np.random.uniform(55, 75)
        }
        chaside_scores = {
            'c': np.random.randint(5, 9), 'h': np.random.randint(2, 5),
            'a': np.random.randint(1, 4), 's': np.random.randint(4, 7),
            'i': np.random.randint(9, 14), 'd': np.random.randint(2, 5),
            'e': np.random.randint(8, 12)
        }
    
    elif student_type == 'humanistico_puro':
        academic_scores = {
            'matematicas_exactas': np.random.uniform(55, 75),
            'ciencias_naturales': np.random.uniform(55, 75),
            'comunicacion_lenguaje': np.random.uniform(80, 95),
            'ciencias_sociales': np.random.uniform(85, 95),
            'artes_expresion': np.random.uniform(65, 85),
            'educacion_fisica': np.random.uniform(55, 75)
        }
        chaside_scores = {
            'c': np.random.randint(6, 10), 'h': np.random.randint(10, 14),
            'a': np.random.randint(5, 9), 's': np.random.randint(3, 6),
            'i': np.random.randint(1, 4), 'd': np.random.randint(4, 7),
            'e': np.random.randint(2, 5)
        }
    
    elif student_type == 'artistico_creativo':
        academic_scores = {
            'matematicas_exactas': np.random.uniform(50, 70),
            'ciencias_naturales': np.random.uniform(55, 75),
            'comunicacion_lenguaje': np.random.uniform(70, 90),
            'ciencias_sociales': np.random.uniform(65, 80),
            'artes_expresion': np.random.uniform(85, 95),
            'educacion_fisica': np.random.uniform(60, 80)
        }
        chaside_scores = {
            'c': np.random.randint(3, 6), 'h': np.random.randint(6, 10),
            'a': np.random.randint(10, 14), 's': np.random.randint(2, 5),
            'i': np.random.randint(3, 7), 'd': np.random.randint(1, 4),
            'e': np.random.randint(2, 5)
        }
    
    elif student_type == 'cientifico_investigador':
        academic_scores = {
            'matematicas_exactas': np.random.uniform(75, 90),
            'ciencias_naturales': np.random.uniform(85, 95),
            'comunicacion_lenguaje': np.random.uniform(60, 80),
            'ciencias_sociales': np.random.uniform(55, 75),
            'artes_expresion': np.random.uniform(50, 70),
            'educacion_fisica': np.random.uniform(55, 75)
        }
        chaside_scores = {
            'c': np.random.randint(4, 7), 'h': np.random.randint(3, 6),
            'a': np.random.randint(1, 4), 's': np.random.randint(7, 11),
            'i': np.random.randint(6, 9), 'd': np.random.randint(2, 5),
            'e': np.random.randint(10, 14)
        }
    
    else:  # equilibrado_versatil
        base_score = np.random.uniform(65, 80)
        variation = 10
        academic_scores = {
            'matematicas_exactas': max(51, min(100, base_score + np.random.uniform(-variation, variation))),
            'ciencias_naturales': max(51, min(100, base_score + np.random.uniform(-variation, variation))),
            'comunicacion_lenguaje': max(51, min(100, base_score + np.random.uniform(-variation, variation))),
            'ciencias_sociales': max(51, min(100, base_score + np.random.uniform(-variation, variation))),
            'artes_expresion': max(51, min(100, base_score + np.random.uniform(-variation, variation))),
            'educacion_fisica': max(51, min(100, base_score + np.random.uniform(-variation, variation)))
        }
        chaside_scores = {
            'c': np.random.randint(5, 9), 'h': np.random.randint(5, 9),
            'a': np.random.randint(5, 9), 's': np.random.randint(5, 9),
            'i': np.random.randint(5, 9), 'd': np.random.randint(5, 9),
            'e': np.random.randint(5, 9)
        }
    
    return academic_scores, chaside_scores

def find_best_career_for_profile_improved(chaside_scores, careers, academic_scores):
    """Encuentra la mejor carrera considerando CHASIDE y rendimiento académico"""
    best_career = None
    best_score = 0
    
    for career in careers:
        # Score CHASIDE
        chaside_score = (
            chaside_scores['c'] * (career.area_c or 0) +
            chaside_scores['h'] * (career.area_h or 0) +
            chaside_scores['a'] * (career.area_a or 0) +
            chaside_scores['s'] * (career.area_s or 0) +
            chaside_scores['i'] * (career.area_i or 0) +
            chaside_scores['d'] * (career.area_d or 0) +
            chaside_scores['e'] * (career.area_e or 0)
        )
        
        # Bonus académico
        academic_avg = np.mean(list(academic_scores.values()))
        academic_bonus = 0
        
        if academic_avg >= 80:
            academic_bonus = chaside_score * 0.2  # 20% bonus
        elif academic_avg >= 70:
            academic_bonus = chaside_score * 0.1  # 10% bonus
        
        final_score = chaside_score + academic_bonus
        
        if final_score > best_score:
            best_score = final_score
            best_career = career
    
    return best_career

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 ¡ENTRENAMIENTO COMPLETADO!")
        print("🤖 Tu sistema ahora usa Inteligencia Artificial")
        print("🚀 Ejecuta: python app.py para probar")
    else:
        print("\n⚠️ Entrenamiento no completado")
        print("💡 El sistema funcionará con reglas mejoradas")
    
    exit(0 if success else 1)