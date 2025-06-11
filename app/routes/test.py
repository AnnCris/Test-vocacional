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

bp = Blueprint('test', __name__, url_prefix='/test')

@bp.route('/start')
@login_required
def start_test():
    """Página de inicio del test vocacional"""
    # Verificar si el estudiante ya ha realizado el test
    student = Student.query.filter_by(user_id=current_user.id).first()
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

@bp.route('/process-results')
@login_required
def process_results():
    """Procesar los resultados del test y generar recomendaciones"""
    # Verificar si hay respuestas en la sesión
    if 'answers' not in session or not session['answers']:
        flash('No hay respuestas para procesar. Por favor, realiza el test.', 'warning')
        return redirect(url_for('test.start_test'))
    
    # Obtener respuestas y procesar test
    answers = session.get('answers', {})
    
    # Verificar que haya suficientes respuestas
    if len(answers) < 50:  # Al menos la mitad de las preguntas
        flash('Por favor, completa más preguntas antes de procesar los resultados.', 'warning')
        return redirect(url_for('test.question', question_number=len(answers)+1))
    
    try:
        test_chaside = TestChaside()
        scores = test_chaside.calculate_scores(answers)
        
        # Guardar respuestas del test en la base de datos
        student = Student.query.filter_by(user_id=current_user.id).first()
        
        # Crear objeto de respuesta
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
        
        # Obtener áreas recomendadas
        recommended_areas = test_chaside.get_recommended_areas(scores, top_n=2)
        print(f"Áreas recomendadas: {recommended_areas}")
        
        # Generar recomendaciones de carreras
        for area_code, score in recommended_areas:
            # Buscar carreras con alto peso en esta área
            area_field = f'area_{area_code.lower()}'
            careers = Career.query.filter(getattr(Career, area_field) >= 0.5).limit(3).all()
            
            # Si no hay carreras que cumplan el criterio, buscar con un umbral más bajo
            if not careers:
                careers = Career.query.filter(getattr(Career, area_field) >= 0.3).limit(3).all()
            
            # Crear recomendaciones
            for rank, career in enumerate(careers, 1):
                try:
                    # Calcular compatibilidad
                    compatibility = calculate_compatibility(student, career, area_code, scores)
                    
                    # Crear explicación
                    explanation = create_explanation(student, career, area_code, test_chaside)
                    
                    # Guardar recomendación
                    recommendation = Recommendation(
                        student_id=student.id,
                        career_id=career.id,
                        score=compatibility,
                        rank=rank,
                        explanation=explanation,
                        model_used='rule_based'
                    )
                    db.session.add(recommendation)
                except Exception as e:
                    print(f"Error procesando carrera {career.name}: {e}")
                    # Continuar con la siguiente carrera en caso de error
                    continue
        
        # Guardar cambios en la base de datos
        db.session.commit()
        
        # Limpiar sesión de respuestas
        session.pop('answers', None)
        
        # Mostrar mensaje de éxito
        flash('¡Test completado! Aquí están tus resultados y recomendaciones.', 'success')
        
        # Redirigir a resultados
        return redirect(url_for('test.test_results'))
        
    except Exception as e:
        # En caso de error, mostrar mensaje y registrar el error
        flash(f'Ocurrió un error al procesar los resultados: {str(e)}', 'danger')
        print(f"Error en process_results: {e}")
        return redirect(url_for('test.start_test'))
    
# No modificamos estas funciones, las dejamos igual
def calculate_compatibility(student, career, area_code, scores):
    """Calcular la compatibilidad entre un estudiante y una carrera basado en el área y notas"""
    # Obtener puntaje del área
    area_score = scores[area_code]['total'] / 10.0  # Normalizar a escala 0-1
    
    # Mapear áreas a las materias relacionadas
    area_subject_mapping = {
        'C': ['math_score', 'social_science_score'],
        'H': ['language_score', 'social_science_score'],
        'A': ['arts_score', 'language_score'],
        'S': ['science_score', 'math_score'],
        'I': ['math_score', 'science_score'],
        'D': ['social_science_score', 'math_score'],
        'E': ['science_score', 'math_score']
    }
    
    # Calcular promedio de notas relacionadas al área
    related_subjects = area_subject_mapping.get(area_code, [])
    subject_scores = []
    
    # Recopilar las puntuaciones de las materias, asegurando que no hay None
    for subject in related_subjects:
        score = getattr(student, subject, None)
        if score is not None:  # Solo agregar si no es None
            subject_scores.append(score)
        else:
            subject_scores.append(0.0)  # Valor predeterminado si es None
    
    # Calcular promedio de forma segura
    avg_subject_score = sum(subject_scores) / len(subject_scores) if subject_scores else 0.0
    
    # Normalizar a escala 0-1
    normalized_subject_score = avg_subject_score / 10.0
    
    # Calcular puntuación de compatibilidad (combinar test y notas)
    compatibility = (area_score * 0.7) + (normalized_subject_score * 0.3)
    
    # Ajustar según el peso de la carrera en ese área
    # Asegurarse de que el área existe en la carrera
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
        radar_chart = None
        bar_chart = None
    
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
    
    # Eliminar test y recomendaciones anteriores
    TestAnswer.query.filter_by(student_id=student.id).delete()
    Recommendation.query.filter_by(student_id=student.id).delete()
    db.session.commit()
    
    flash('Puedes volver a realizar el test vocacional', 'info')
    return redirect(url_for('test.start_test'))