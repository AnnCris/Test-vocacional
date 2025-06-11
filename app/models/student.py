from app import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    birth_date = db.Column(db.Date)
    grade = db.Column(db.String(20))  # 4to, 5to o 6to de secundaria
    school = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Notas académicas del sistema educativo boliviano (escala 1-100)
    # Área de Matemáticas y Ciencias Exactas
    matematicas_score = db.Column(db.Integer)  # Matemáticas
    fisica_score = db.Column(db.Integer)       # Física
    quimica_score = db.Column(db.Integer)      # Química
    
    # Área de Ciencias Naturales y Biología
    biologia_score = db.Column(db.Integer)     # Biología/Ciencias Naturales
    
    # Área de Comunicación y Lenguaje
    lenguaje_score = db.Column(db.Integer)     # Lenguaje y Comunicación
    ingles_score = db.Column(db.Integer)       # Inglés/Lengua Extranjera
    
    # Área de Ciencias Sociales y Humanidades
    ciencias_sociales_score = db.Column(db.Integer)  # Historia, Geografía, Cívica
    filosofia_score = db.Column(db.Integer)           # Filosofía/Psicología
    valores_score = db.Column(db.Integer)             # Valores/Religión
    
    # Área Artística y Expresiva
    artes_plasticas_score = db.Column(db.Integer)    # Artes Plásticas y Visuales
    educacion_musical_score = db.Column(db.Integer)  # Educación Musical
    
    # Área de Educación Física
    educacion_fisica_score = db.Column(db.Integer)   # Educación Física
    
    # Relaciones
    test_answers = db.relationship('TestAnswer', backref='student', lazy='dynamic')
    recommendations = db.relationship('Recommendation', backref='student', lazy='dynamic')
    
    def get_average_by_area(self):
        """Calcula promedios por área de conocimiento"""
        areas = {
            'matematicas_exactas': [
                self.matematicas_score, 
                self.fisica_score, 
                self.quimica_score
            ],
            'ciencias_naturales': [
                self.biologia_score
            ],
            'comunicacion_lenguaje': [
                self.lenguaje_score, 
                self.ingles_score
            ],
            'ciencias_sociales': [
                self.ciencias_sociales_score, 
                self.filosofia_score, 
                self.valores_score
            ],
            'artes_expresion': [
                self.artes_plasticas_score, 
                self.educacion_musical_score
            ],
            'educacion_fisica': [
                self.educacion_fisica_score
            ]
        }
        
        averages = {}
        for area, scores in areas.items():
            valid_scores = [score for score in scores if score is not None]
            if valid_scores:
                averages[area] = sum(valid_scores) / len(valid_scores)
            else:
                averages[area] = 0
        
        return averages
    
    def get_overall_average(self):
        """Calcula el promedio general del estudiante"""
        all_scores = [
            self.matematicas_score, self.fisica_score, self.quimica_score,
            self.biologia_score, self.lenguaje_score, self.ingles_score,
            self.ciencias_sociales_score, self.filosofia_score, self.valores_score,
            self.artes_plasticas_score, self.educacion_musical_score,
            self.educacion_fisica_score
        ]
        
        valid_scores = [score for score in all_scores if score is not None]
        if valid_scores:
            return sum(valid_scores) / len(valid_scores)
        return 0
    
    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'