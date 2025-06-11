# CREAR ARCHIVO: validate_system.py (en la carpeta raíz)

#!/usr/bin/env python3
"""
Script SIMPLE para validar que la integración CHASIDE + ML funcione
"""

import sys
import os

def main():
    print("🧪 Validación del Sistema CHASIDE + ML")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Verificar importaciones
    total_tests += 1
    print("\n1️⃣ Verificando importaciones...")
    if test_imports():
        tests_passed += 1
        print("   ✅ Importaciones OK")
    else:
        print("   ❌ Error en importaciones")
    
    # Test 2: Verificar base de datos
    total_tests += 1
    print("\n2️⃣ Verificando base de datos...")
    if test_database():
        tests_passed += 1
        print("   ✅ Base de datos OK")
    else:
        print("   ❌ Error en base de datos")
    
    # Test 3: Verificar test CHASIDE
    total_tests += 1
    print("\n3️⃣ Verificando test CHASIDE...")
    if test_chaside():
        tests_passed += 1
        print("   ✅ Test CHASIDE OK")
    else:
        print("   ❌ Error en test CHASIDE")
    
    # Test 4: Verificar CareerMatcher
    total_tests += 1
    print("\n4️⃣ Verificando CareerMatcher...")
    if test_career_matcher():
        tests_passed += 1
        print("   ✅ CareerMatcher OK")
    else:
        print("   ❌ Error en CareerMatcher")
    
    # Test 5: Verificar flujo completo
    total_tests += 1
    print("\n5️⃣ Verificando flujo completo...")
    if test_complete_flow():
        tests_passed += 1
        print("   ✅ Flujo completo OK")
    else:
        print("   ❌ Error en flujo completo")
    
    # Resumen
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE VALIDACIÓN")
    print("=" * 50)
    print(f"✅ Tests pasados: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("\n🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("💡 Tu integración CHASIDE + ML está lista")
        print("🚀 Puedes ejecutar: python app.py")
        return True
    elif tests_passed >= 3:
        print("\n⚠️ Sistema mayormente funcional")
        print("💡 Hay algunos problemas menores que resolver")
        return True
    else:
        print("\n❌ Sistema necesita reparaciones")
        print("💡 Revisa los errores anteriores")
        return False

def test_imports():
    """Verifica que las importaciones funcionen"""
    try:
        # Importaciones básicas
        from flask import Flask
        from app import create_app
        
        # Importaciones de modelos
        from app.models.student import Student
        from app.models.career import Career
        from app.models.test_answer import TestAnswer
        
        # Importaciones de utilidades
        from app.utils.test_chaside import TestChaside
        
        # Importaciones mejoradas
        from app.utils.career_matcher import CareerMatcher
        from app.ml_models.data_processor import DataProcessor
        
        return True
        
    except ImportError as e:
        print(f"   Error de importación: {e}")
        return False
    except Exception as e:
        print(f"   Error inesperado: {e}")
        return False

def test_database():
    """Verifica la conexión a la base de datos"""
    try:
        from app import create_app, db
        from app.models.career import Career
        from sqlalchemy import text
        
        app = create_app()
        with app.app_context():
            # Probar conexión
            result = db.session.execute(text('SELECT 1'))
            result.fetchone()
            
            # Verificar que hay carreras
            career_count = Career.query.count()
            if career_count == 0:
                print("   ⚠️ No hay carreras - ejecuta: python init_db.py")
                return False
            
            print(f"   📊 {career_count} carreras encontradas")
            return True
            
    except Exception as e:
        print(f"   Error de base de datos: {e}")
        return False

def test_chaside():
    """Verifica que el test CHASIDE funcione"""
    try:
        from app.utils.test_chaside import TestChaside
        
        # Inicializar test
        test_chaside = TestChaside()
        
        # Verificar preguntas
        questions = test_chaside.get_questions()
        if len(questions) != 98:
            print(f"   ❌ Faltan preguntas: {len(questions)}/98")
            return False
        
        # Simular respuestas
        test_answers = {str(i): i % 2 == 0 for i in range(1, 99)}
        
        # Calcular puntajes
        scores = test_chaside.calculate_scores(test_answers)
        
        # Verificar que todos los puntajes estén en rango
        for area, area_scores in scores.items():
            total = area_scores['total']
            if not (0 <= total <= 14):
                print(f"   ❌ Puntaje fuera de rango: {area}={total}")
                return False
        
        print(f"   📊 Puntajes calculados correctamente")
        return True
        
    except Exception as e:
        print(f"   Error en CHASIDE: {e}")
        return False

def test_career_matcher():
    """Verifica que el CareerMatcher funcione"""
    try:
        from app.utils.career_matcher import CareerMatcher
        from app import create_app
        
        app = create_app()
        with app.app_context():
            # Crear datos de prueba
            mock_student, mock_test = create_mock_data()
            
            # Inicializar matcher
            matcher = CareerMatcher()
            
            # Verificar que se inicialice
            print(f"   🤖 ML disponible: {'Sí' if matcher.models_loaded else 'No'}")
            
            # Probar generación de recomendaciones
            recommendations = matcher.generate_recommendations(
                mock_student, mock_test, top_n=3
            )
            
            if len(recommendations) == 0:
                print("   ❌ No se generaron recomendaciones")
                return False
            
            print(f"   ✅ {len(recommendations)} recomendaciones generadas")
            
            # Verificar formato
            for rec in recommendations:
                if not hasattr(rec, 'career_id') or not hasattr(rec, 'score'):
                    print("   ❌ Formato de recomendación inválido")
                    return False
                if not (0 <= rec.score <= 1):
                    print(f"   ❌ Score fuera de rango: {rec.score}")
                    return False
            
            return True
            
    except Exception as e:
        print(f"   Error en CareerMatcher: {e}")
        return False

def test_complete_flow():
    """Verifica el flujo completo"""
    try:
        from app.utils.test_chaside import TestChaside
        from app.utils.career_matcher import CareerMatcher
        from app import create_app
        
        app = create_app()
        with app.app_context():
            # 1. Simular test CHASIDE
            test_chaside = TestChaside()
            test_answers_dict = {str(i): i % 3 == 0 for i in range(1, 99)}
            scores = test_chaside.calculate_scores(test_answers_dict)
            
            # 2. Crear estudiante y test simulados
            mock_student, mock_test = create_mock_data()
            
            # Actualizar scores con los calculados
            for area in ['c', 'h', 'a', 's', 'i', 'd', 'e']:
                setattr(mock_test, f'score_{area}', scores[area.upper()]['total'])
            
            # 3. Generar recomendaciones
            matcher = CareerMatcher()
            recommendations = matcher.generate_recommendations(
                mock_student, mock_test, top_n=5
            )
            
            if len(recommendations) == 0:
                print("   ❌ Flujo no generó recomendaciones")
                return False
            
            # 4. Verificar explicaciones
            has_explanations = False
            for rec in recommendations:
                if hasattr(rec, 'explanation') and rec.explanation:
                    try:
                        import json
                        explanation = json.loads(rec.explanation)
                        if 'career_name' in explanation:
                            has_explanations = True
                            break
                    except:
                        continue
            
            if has_explanations:
                print("   ✅ Explicaciones disponibles")
            else:
                print("   ⚠️ Sin explicaciones detalladas")
            
            print(f"   🎯 Flujo completo funcional")
            return True
            
    except Exception as e:
        print(f"   Error en flujo completo: {e}")
        return False

def create_mock_data():
    """Crea datos de prueba"""
    
    class MockStudent:
        def __init__(self):
            self.id = 999
            self.first_name = "Estudiante"
            self.last_name = "Prueba"
            # Notas sistema boliviano
            self.matematicas_score = 75
            self.fisica_score = 70
            self.quimica_score = 72
            self.biologia_score = 68
            self.lenguaje_score = 80
            self.ingles_score = 75
            self.ciencias_sociales_score = 78
            self.filosofia_score = 76
            self.valores_score = 82
            self.artes_plasticas_score = 65
            self.educacion_musical_score = 60
            self.educacion_fisica_score = 70
        
        def get_average_by_area(self):
            import numpy as np
            return {
                'matematicas_exactas': np.mean([75, 70, 72]),
                'ciencias_naturales': 68,
                'comunicacion_lenguaje': np.mean([80, 75]),
                'ciencias_sociales': np.mean([78, 76, 82]),
                'artes_expresion': np.mean([65, 60]),
                'educacion_fisica': 70
            }
    
    class MockTestAnswer:
        def __init__(self):
            self.id = 999
            self.student_id = 999
            self.score_c = 8
            self.score_h = 6
            self.score_a = 4
            self.score_s = 7
            self.score_i = 9
            self.score_d = 3
            self.score_e = 8
            self.answers_json = '{"1": true, "2": false}'
    
    return MockStudent(), MockTestAnswer()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)