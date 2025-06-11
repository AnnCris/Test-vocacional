from app import db

class Faculty(db.Model):
    __tablename__ = 'faculties'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # Relación con carreras
    careers = db.relationship('Career', backref='faculty', lazy='dynamic')
    
    def __repr__(self):
        return f'<Faculty {self.name}>'