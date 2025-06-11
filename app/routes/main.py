from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.models.student import Student

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Imprimir la URL generada
    test_url = url_for('test.start_test')
    print(f"URL generada para el test: {test_url}")
    
    return render_template('index.html')

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Perfil del estudiante con información académica boliviana"""
    student = Student.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        # Actualizar información personal
        student.first_name = request.form.get('first_name')
        student.last_name = request.form.get('last_name')
        student.birth_date = request.form.get('birth_date')
        student.grade = request.form.get('grade')
        student.school = request.form.get('school')
        
        # Actualizar calificaciones del sistema boliviano (1-100)
        # Área de Matemáticas y Ciencias Exactas
        student.matematicas_score = int(request.form.get('matematicas_score') or 0) or None
        student.fisica_score = int(request.form.get('fisica_score') or 0) or None
        student.quimica_score = int(request.form.get('quimica_score') or 0) or None
        
        # Área de Ciencias Naturales
        student.biologia_score = int(request.form.get('biologia_score') or 0) or None
        
        # Área de Comunicación y Lenguaje
        student.lenguaje_score = int(request.form.get('lenguaje_score') or 0) or None
        student.ingles_score = int(request.form.get('ingles_score') or 0) or None
        
        # Área de Ciencias Sociales
        student.ciencias_sociales_score = int(request.form.get('ciencias_sociales_score') or 0) or None
        student.filosofia_score = int(request.form.get('filosofia_score') or 0) or None
        student.valores_score = int(request.form.get('valores_score') or 0) or None
        
        # Área Artística
        student.artes_plasticas_score = int(request.form.get('artes_plasticas_score') or 0) or None
        student.educacion_musical_score = int(request.form.get('educacion_musical_score') or 0) or None
        
        # Educación Física
        student.educacion_fisica_score = int(request.form.get('educacion_fisica_score') or 0) or None
        
        try:
            db.session.commit()
            flash('Perfil actualizado correctamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el perfil: {str(e)}', 'danger')
        
        return redirect(url_for('main.profile'))
    
    return render_template('profile.html', student=student)

@bp.route('/about')
def about():
    """Información sobre el sistema de recomendación"""
    return render_template('about.html')

@bp.route('/careers')
def careers():
    """Lista de todas las carreras en el sistema"""
    from app.models.career import Career, Aptitude
    from app.models.faculty import Faculty
    
    careers = Career.query.all()
    faculties = Faculty.query.all()
    
    return render_template('careers.html', careers=careers, faculties=faculties)

@bp.route('/faculties')
def faculties():
    """Lista de todas las facultades en el sistema"""
    from app.models.faculty import Faculty
    
    faculties = Faculty.query.all()
    
    return render_template('faculties.html', faculties=faculties)