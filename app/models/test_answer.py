from app import db
from datetime import datetime

class TestAnswer(db.Model):
    __tablename__ = 'test_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    test_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Resultados del test CHASIDE
    score_c = db.Column(db.Integer, default=0)  # Administrativas y contables
    score_h = db.Column(db.Integer, default=0)  # Humanísticas y sociales
    score_a = db.Column(db.Integer, default=0)  # Artísticas
    score_s = db.Column(db.Integer, default=0)  # Medicina y ciencias de la salud
    score_i = db.Column(db.Integer, default=0)  # Ingeniería y computación
    score_d = db.Column(db.Integer, default=0)  # Defensa y seguridad
    score_e = db.Column(db.Integer, default=0)  # Ciencias exactas y agrarias
    
    # Almacenar respuestas detalladas (formato JSON)
    answers_json = db.Column(db.Text)
    
    def __repr__(self):
        return f'<TestAnswer {self.id} - Student {self.student_id}>'