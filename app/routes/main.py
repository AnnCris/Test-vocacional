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
    """Perfil del estudiante con su información académica"""
    student = Student.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        # Actualizar información del estudiante
        student.first_name = request.form.get('first_name')
        student.last_name = request.form.get('last_name')
        student.birth_date = request.form.get('birth_date')
        student.grade = request.form.get('grade')
        student.school = request.form.get('school')
        
        # Actualizar notas académicas
        student.math_score = float(request.form.get('math_score', 0))
        student.science_score = float(request.form.get('science_score', 0))
        student.language_score = float(request.form.get('language_score', 0))
        student.social_science_score = float(request.form.get('social_science_score', 0))
        student.arts_score = float(request.form.get('arts_score', 0))
        
        db.session.commit()
        flash('Perfil actualizado correctamente', 'success')
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