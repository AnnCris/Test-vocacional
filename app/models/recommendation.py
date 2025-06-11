from app import db
from datetime import datetime

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    career_id = db.Column(db.Integer, db.ForeignKey('careers.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)  # Puntuación de coincidencia
    rank = db.Column(db.Integer, nullable=False)  # Posición en el ranking (1, 2, 3...)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Almacenar justificación (formato JSON)
    explanation = db.Column(db.Text)
    
    # Modelo utilizado para la recomendación
    model_used = db.Column(db.String(50))  # 'logistic', 'tree', 'knn', 'neural_network'
    
    def __repr__(self):
        return f'<Recommendation {self.id} - Student {self.student_id} - Career {self.career_id}>'