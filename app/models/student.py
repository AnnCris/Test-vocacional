from app import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    birth_date = db.Column(db.Date)
    grade = db.Column(db.String(20))  # 5to o 6to de secundaria
    school = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Notas académicas por área
    math_score = db.Column(db.Float)
    science_score = db.Column(db.Float)
    language_score = db.Column(db.Float)
    social_science_score = db.Column(db.Float)
    arts_score = db.Column(db.Float)
    
    test_answers = db.relationship('TestAnswer', backref='student', lazy='dynamic')
    recommendations = db.relationship('Recommendation', backref='student', lazy='dynamic')
    
    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'