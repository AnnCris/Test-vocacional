from app import db

# Tabla de asociación entre carreras y aptitudes
career_aptitude = db.Table('career_aptitude',
    db.Column('career_id', db.Integer, db.ForeignKey('careers.id'), primary_key=True),
    db.Column('aptitude_id', db.Integer, db.ForeignKey('aptitudes.id'), primary_key=True)
)

class Career(db.Model):
    __tablename__ = 'careers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'), nullable=False)
    
    # Áreas principales relacionadas con el test CHASIDE
    area_c = db.Column(db.Float, default=0.0)  # Administrativas y contables
    area_h = db.Column(db.Float, default=0.0)  # Humanísticas y sociales
    area_a = db.Column(db.Float, default=0.0)  # Artísticas
    area_s = db.Column(db.Float, default=0.0)  # Medicina y ciencias de la salud
    area_i = db.Column(db.Float, default=0.0)  # Ingeniería y computación
    area_d = db.Column(db.Float, default=0.0)  # Defensa y seguridad
    area_e = db.Column(db.Float, default=0.0)  # Ciencias exactas y agrarias
    
    # Relación con recomendaciones
    recommendations = db.relationship('Recommendation', backref='career', lazy='dynamic')
    
    # Relación con aptitudes
    aptitudes = db.relationship('Aptitude', secondary=career_aptitude, 
                               backref=db.backref('careers', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Career {self.name}>'

class Aptitude(db.Model):
    __tablename__ = 'aptitudes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # Categoría de la aptitud
    
    def __repr__(self):
        return f'<Aptitude {self.name}>'