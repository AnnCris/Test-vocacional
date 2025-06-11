from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_required
from app import db
from app.models.student import Student
from app.models.test_answer import TestAnswer
from app.models.recommendation import Recommendation
from app.models.career import Career
from app.utils.test_chaside import TestChaside
import json
import numpy as np
from datetime import datetime

# Crear el blueprint
bp = Blueprint('test', __name__, url_prefix='/test')

@bp.route('/start')
@login_required
def start_test():
    """Página de inicio del test vocacional"""
    # Verificar si el estudiante ya ha realizado el test
    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        flash('Debes completar tu perfil antes de realizar el test.', 'warning')
        return redirect(url_for('main.profile'))
    
    existing_test = TestAnswer.query.filter_by(student_id=student.id).first()
    
    if existing_test:
        flash('Ya has realizado el test vocacional. Puedes ver tus resultados o volver a realizar el test.', 'info')
        return redirect(url_for('test.test_results'))
    
    # Mostrar página inicial con instrucciones
    return render_template('test/start.html')

@bp.route('/question/<int:question_number>', methods=['GET', 'POST'])
@login_required
def question(question_number=1):
    """Mostrar y procesar cada pregunta del test"""
    # Verificar que el número de pregunta sea válido
    if question_number < 1 or question_number > 98:
        flash('Número de pregunta inválido.', 'danger')
        return redirect(url_for('test.start_test'))
    
    # Inicializar el test
    test_chaside = TestChaside()
    questions = test_chaside.get_questions()
    
    # Obtener la pregunta actual
    current_question_text = questions.get(question_number, "Pregunta no disponible")
    
    # Inicializar o recuperar las respuestas
    if 'answers' not in session:
        session['answers'] = {}
    
    answers = session.get('answers', {})
    
    # Si se ha enviado una respuesta
    if request.method == 'POST':
        answer = request.form.get('answer') == 'yes'
        answers[str(question_number)] = answer
        session['answers'] = answers
        session.modified = True
        
        # Avanzar a la siguiente pregunta
        next_question = question_number + 1
        
        # Verificar si es la última pregunta
        if next_question > 98:
            return redirect(url_for('test.process_results'))
        
        # Redirigir a la siguiente pregunta
        return redirect(url_for('test.question', question_number=next_question))
    
    return render_template('test/question.html', 
                          question_number=question_number,
                          question=current_question_text,
                          total_questions=98)

@bp.route('/comenzar')
@login_required
def comenzar_test():
    """Ruta para comenzar el test - redirige a la primera pregunta"""
    # Limpiar respuestas anteriores en la sesión
    session['answers'] = {}
    session.modified = True
    
    # Redirigir a la primera pregunta
    return redirect(url_for('test.question', question_number=1))

# REEMPLAZA LA FUNCIÓN process_results EN: app/routes/test.py

@bp.route('/process-results')
@login_required
def process_results():
    """Procesar resultados con INTEGRACIÓN ML MEJORADA"""
    
    # Verificar respuestas
    if 'answers' not in session or not session['answers']:
        flash('No hay respuestas para procesar. Por favor, realiza el test.', 'warning')
        return redirect(url_for('test.start_test'))
    
    answers = session.get('answers', {})
    
    if len(answers) < 50:
        flash('Por favor, completa más preguntas antes de procesar los resultados.', 'warning')
        return redirect(url_for('test.question', question_number=len(answers)+1))
    
    try:
        print(f"🔄 Procesando {len(answers)} respuestas con IA...")
        
        # Procesar test CHASIDE
        test_chaside = TestChaside()
        scores = test_chaside.calculate_scores(answers)
        
        # Obtener estudiante
        student = Student.query.filter_by(user_id=current_user.id).first()
        if not student:
            flash('Error: No se encontró el perfil del estudiante.', 'danger')
            return redirect(url_for('main.profile'))
        
        # Limpiar datos anteriores
        existing_test = TestAnswer.query.filter_by(student_id=student.id).first()
        if existing_test:
            db.session.delete(existing_test)
        Recommendation.query.filter_by(student_id=student.id).delete()
        
        # Crear respuesta del test
        test_answer = TestAnswer(
            student_id=student.id,
            score_c=scores['C']['total'],
            score_h=scores['H']['total'],
            score_a=scores['A']['total'],
            score_s=scores['S']['total'],
            score_i=scores['I']['total'],
            score_d=scores['D']['total'],
            score_e=scores['E']['total'],
            answers_json=json.dumps(answers)
        )
        db.session.add(test_answer)
        db.session.flush()
        
        print(f"✅ Test guardado: C={scores['C']['total']}, I={scores['I']['total']}, S={scores['S']['total']}")
        
        # 🤖 GENERAR RECOMENDACIONES CON IA MEJORADA
        try:
            print("🤖 Generando recomendaciones con ML...")
            from app.utils.career_matcher import CareerMatcher
            
            career_matcher = CareerMatcher()
            recommendations = career_matcher.generate_recommendations(
                student, test_answer, top_n=5
            )
            
            if recommendations:
                print(f"✅ {len(recommendations)} recomendaciones con IA generadas")
            else:
                print("⚠️ Usando método de respaldo...")
                recommendations = generate_fallback_recommendations(student, test_answer, scores)
                
        except Exception as e:
            print(f"⚠️ Error en IA, usando respaldo: {e}")
            recommendations = generate_fallback_recommendations(student, test_answer, scores)
        
        # Guardar recomendaciones
        for recommendation in recommendations:
            db.session.add(recommendation)
        
        db.session.commit()
        session.pop('answers', None)
        
        flash('¡Test completado! Recomendaciones generadas con Inteligencia Artificial.', 'success')
        return redirect(url_for('test.test_results'))
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error: {e}")
        flash('Error procesando resultados. Inténtalo de nuevo.', 'danger')
        return redirect(url_for('test.start_test'))


# AGREGAR ESTA FUNCIÓN NUEVA AL FINAL DEL ARCHIVO
def generate_fallback_recommendations(student, test_answer, scores):
    """Genera recomendaciones de respaldo mejoradas"""
    try:
        print("🔄 Generando recomendaciones de respaldo mejoradas...")
        
        from app.utils.test_chaside import TestChaside
        test_chaside = TestChaside()
        
        # Obtener áreas más fuertes
        recommended_areas = test_chaside.get_recommended_areas(scores, top_n=3)
        
        recommendations = []
        rank = 1
        
        for area_code, area_score in recommended_areas:
            if rank > 5:
                break
                
            # Buscar carreras para esta área
            area_field = f'area_{area_code.lower()}'
            careers = Career.query.filter(getattr(Career, area_field) >= 0.4).limit(2).all()
            
            for career in careers:
                if rank > 5:
                    break
                    
                try:
                    # Calcular compatibilidad MEJORADA
                    compatibility = calculate_improved_compatibility(student, career, area_code, scores)
                    
                    # Crear explicación MEJORADA
                    explanation = create_improved_explanation(student, career, area_code, test_chaside)
                    
                    recommendation = Recommendation(
                        student_id=student.id,
                        career_id=career.id,
                        score=compatibility,
                        rank=rank,
                        explanation=explanation,
                        model_used='reglas_mejoradas'
                    )
                    
                    recommendations.append(recommendation)
                    rank += 1
                    
                except Exception as e:
                    print(f"⚠️ Error con carrera {career.name}: {e}")
                    continue
        
        print(f"✅ {len(recommendations)} recomendaciones de respaldo generadas")
        return recommendations
        
    except Exception as e:
        print(f"❌ Error en respaldo: {e}")
        return []


def calculate_improved_compatibility(student, career, area_code, scores):
    """Cálculo de compatibilidad MEJORADO para sistema boliviano"""
    try:
        # Puntaje del área CHASIDE
        area_score = scores[area_code]['total'] / 14.0
        
        # Peso de la carrera en esa área
        area_attr = f'area_{area_code.lower()}'
        career_weight = getattr(career, area_attr, 0.0) or 0.0
        
        # Compatibilidad base
        base_compatibility = area_score * career_weight
        
        # 🇧🇴 BONUS POR RENDIMIENTO ACADÉMICO BOLIVIANO
        areas_avg = student.get_average_by_area()
        overall_avg = np.mean(list(areas_avg.values())) if areas_avg else 51
        
        # Bonus según escala boliviana
        if overall_avg >= 80:
            academic_bonus = 0.3  # Excelente
        elif overall_avg >= 70:
            academic_bonus = 0.2  # Muy bueno
        elif overall_avg >= 60:
            academic_bonus = 0.1  # Bueno
        else:
            academic_bonus = 0.0  # Regular
        
        # Bonus por área académica relevante
        area_academic_bonus = 0.0
        if area_code == 'I':  # Ingeniería
            math_avg = areas_avg.get('matematicas_exactas', 51)
            if math_avg >= 70:
                area_academic_bonus = 0.15
        elif area_code == 'S':  # Salud
            science_avg = areas_avg.get('ciencias_naturales', 51)
            if science_avg >= 70:
                area_academic_bonus = 0.15
        elif area_code == 'H':  # Humanísticas
            lang_avg = areas_avg.get('comunicacion_lenguaje', 51)
            if lang_avg >= 70:
                area_academic_bonus = 0.15
        
        # Compatibilidad final
        final_compatibility = min(
            base_compatibility + (academic_bonus * 0.3) + (area_academic_bonus * 0.2), 
            1.0
        )
        
        return final_compatibility
        
    except Exception as e:
        print(f"Error calculando compatibilidad: {e}")
        return 0.5


def create_improved_explanation(student, career, area_code, test_chaside):
    """Crea explicación MEJORADA para recomendaciones"""
    try:
        area_info = test_chaside.get_area_characteristics(area_code)
        
        # Análisis académico boliviano
        areas_avg = student.get_average_by_area()
        overall_avg = np.mean(list(areas_avg.values())) if areas_avg else 51
        
        # Determinar nivel académico
        if overall_avg >= 80:
            academic_level = "Excelente"
        elif overall_avg >= 70:
            academic_level = "Muy Bueno"
        elif overall_avg >= 60:
            academic_level = "Bueno"
        else:
            academic_level = "Regular"
        
        explanation = {
            "career_name": career.name,
            "faculty_name": career.faculty.name if career.faculty else "No especificada",
            "area_code": area_code,
            "area_name": area_info.get('name', ''),
            "academic_level": academic_level,
            "overall_average": round(overall_avg, 1),
            "recommendation_reason": f"Tu perfil muestra fuerte afinidad con {area_info.get('name', '')} y un rendimiento académico {academic_level} ({overall_avg:.1f}/100) que te prepara bien para {career.name}.",
            "career_description": career.description or "Carrera con excelentes perspectivas.",
            "system_used": "reglas_mejoradas_boliviano"
        }
        
        return json.dumps(explanation)
        
    except Exception as e:
        print(f"Error creando explicación: {e}")
        return json.dumps({"error": "No se pudo generar explicación"})
    
    
def calculate_compatibility(student, career, area_code, scores):
    """Calcular la compatibilidad entre un estudiante y una carrera basado en el área y notas (Sistema Boliviano)"""
    # Obtener puntaje del área
    area_score = scores[area_code]['total'] / 10.0  # Normalizar a escala 0-1
    
    # Mapear áreas CHASIDE a las materias bolivianas relacionadas
    area_subject_mapping = {
        'C': ['matematicas_score', 'ciencias_sociales_score'],  # Administrativas
        'H': ['lenguaje_score', 'ciencias_sociales_score', 'filosofia_score'],  # Humanísticas
        'A': ['artes_plasticas_score', 'educacion_musical_score'],  # Artísticas
        'S': ['biologia_score', 'quimica_score'],  # Salud
        'I': ['matematicas_score', 'fisica_score', 'quimica_score'],  # Ingeniería
        'D': ['ciencias_sociales_score', 'educacion_fisica_score'],  # Defensa
        'E': ['fisica_score', 'quimica_score', 'biologia_score']  # Ciencias exactas
    }
    
    # Calcular promedio de notas relacionadas al área (sistema boliviano 1-100)
    related_subjects = area_subject_mapping.get(area_code, [])
    subject_scores = []
    
    # Recopilar las puntuaciones de las materias, asegurando que no hay None
    for subject in related_subjects:
        score = getattr(student, subject, None)
        if score is not None and score > 0:  # Solo agregar si no es None y mayor que 0
            subject_scores.append(score)
        else:
            subject_scores.append(51.0)  # Valor por defecto (51/100 = aprobatorio mínimo)
    
    # Calcular promedio de forma segura
    avg_subject_score = sum(subject_scores) / len(subject_scores) if subject_scores else 51.0
    
    # Normalizar a escala 0-1 (51 es el mínimo aprobatorio en Bolivia)
    # Rango: 51-100 -> 0-1
    normalized_subject_score = max((avg_subject_score - 51) / 49.0, 0.0)  # (score - 51) / (100 - 51)
    
    # Calcular puntuación de compatibilidad (combinar test y notas)
    compatibility = (area_score * 0.7) + (normalized_subject_score * 0.3)
    
    # Ajustar según el peso de la carrera en ese área
    area_attr = f'area_{area_code.lower()}'
    area_weight = getattr(career, area_attr, 0.0)
    
    # Asegurarse de que area_weight no es None
    if area_weight is None:
        area_weight = 0.0
    
    return compatibility * area_weight

def create_explanation(student, career, area_code, test_chaside):
    """Crear una explicación detallada para la recomendación"""
    # Obtener características del área
    area_info = test_chaside.get_area_characteristics(area_code)
    
    # Crear explicación
    explanation = {
        "area_code": area_code,
        "area_name": area_info.get('name', ''),
        "career_name": career.name,
        "career_description": career.description,
        "interests": area_info.get('interests', []),
        "aptitudes": area_info.get('aptitudes', []),
        "related_careers": test_chaside.get_careers_by_area(area_code)[:5],
        "recommendation_reason": f"Basado en tus respuestas, muestras una fuerte inclinación hacia el área {area_info.get('name', '')}, que se alinea bien con la carrera de {career.name}."
    }
    
    return json.dumps(explanation)

@bp.route('/results')
@login_required
def test_results():
    """Mostrar resultados del test y recomendaciones"""
    student = Student.query.filter_by(user_id=current_user.id).first()
    
    if not student:
        flash('Debes completar tu perfil antes de ver los resultados.', 'warning')
        return redirect(url_for('main.profile'))
    
    # Verificar si ha realizado el test
    test_answers = TestAnswer.query.filter_by(student_id=student.id).order_by(TestAnswer.test_date.desc()).first()
    
    if not test_answers:
        flash('Aún no has realizado el test vocacional', 'info')
        return redirect(url_for('test.start_test'))
    
    # Obtener resultados y recomendaciones
    scores = {
        'C': test_answers.score_c,
        'H': test_answers.score_h,
        'A': test_answers.score_a,
        'S': test_answers.score_s,
        'I': test_answers.score_i,
        'D': test_answers.score_d,
        'E': test_answers.score_e
    }
    
    recommendations = Recommendation.query.filter_by(student_id=student.id).order_by(Recommendation.score.desc()).all()
    
    # Generar gráfico de radar para visualización
    radar_chart = None
    bar_chart = None
    try:
        from app.utils.chart_generator import ChartGenerator
        radar_chart = ChartGenerator.generate_radar_chart(scores)
        
        # Preparar datos para gráfico de barras de carreras
        career_scores = []
        for rec in recommendations[:5]:
            career = Career.query.get(rec.career_id)
            if career:
                career_scores.append((career.name, rec.score))
        
        bar_chart = ChartGenerator.generate_bar_chart(career_scores)
    except Exception as e:
        print(f"Error generando gráficos: {e}")
    
    # Preparar datos para visualización
    test_chaside = TestChaside()
    area_explanations = {}
    for area_code in ['C', 'H', 'A', 'S', 'I', 'D', 'E']:
        area_explanations[area_code] = test_chaside.get_area_characteristics(area_code)
    
    # Obtener carreras recomendadas con detalles
    recommended_careers = []
    for rec in recommendations[:5]:  # Top 5 recomendaciones
        career = Career.query.get(rec.career_id)
        if not career:
            continue
            
        try:
            explanation = json.loads(rec.explanation) if rec.explanation else {}
        except:
            explanation = {}
        
        recommended_careers.append({
            'career': career,
            'score': rec.score * 100,  # Convertir a porcentaje
            'rank': rec.rank,
            'explanation': explanation
        })
    
    return render_template('test/results.html',
                          test_date=test_answers.test_date,
                          scores=scores,
                          recommended_careers=recommended_careers,
                          area_explanations=area_explanations,
                          radar_chart=radar_chart,
                          bar_chart=bar_chart)

@bp.route('/retake')
@login_required
def retake_test():
    """Volver a realizar el test vocacional"""
    student = Student.query.filter_by(user_id=current_user.id).first()
    
    if not student:
        flash('Debes completar tu perfil primero.', 'warning')
        return redirect(url_for('main.profile'))
    
    # Eliminar test y recomendaciones anteriores
    TestAnswer.query.filter_by(student_id=student.id).delete()
    Recommendation.query.filter_by(student_id=student.id).delete()
    db.session.commit()
    
    flash('Puedes volver a realizar el test vocacional', 'info')
    return redirect(url_for('test.start_test'))