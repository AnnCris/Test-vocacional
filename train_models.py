# train_models.py
from app import create_app, db
from app.models.student import Student
from app.models.test_answer import TestAnswer
from app.models.career import Career, Aptitude
from app.models.recommendation import Recommendation
from app.ml_models.data_processor import DataProcessor
from app.ml_models.ensemble import EnsembleRecommender
import pandas as pd
import numpy as np
import os

def train_models():
    print("Iniciando entrenamiento de modelos...")
    app = create_app()
    with app.app_context():
        # Verificar si hay suficientes datos
        students = Student.query.all()
        test_answers = TestAnswer.query.all()
        
        if len(students) < 5 or len(test_answers) < 5:
            print(f"No hay suficientes datos para entrenar los modelos. Se necesitan al menos 5 registros. Actuales: {len(test_answers)}")
            return False
        
        # Preparar datos para entrenamiento
        data_processor = DataProcessor()
        training_data = []
        labels = []
        
        # Recopilar datos de estudiantes con recomendaciones
        recommendations = Recommendation.query.filter_by(rank=1).all()  # Solo las mejores recomendaciones
        for rec in recommendations:
            student = Student.query.get(rec.student_id)
            test_answer = TestAnswer.query.filter_by(student_id=student.id).order_by(TestAnswer.test_date.desc()).first()
            
            if not student or not test_answer:
                continue
            
            # Procesar datos del estudiante
            student_data = {
                'math_score': student.math_score if student.math_score is not None else 5.0,
                'science_score': student.science_score if student.science_score is not None else 5.0,
                'language_score': student.language_score if student.language_score is not None else 5.0,
                'social_science_score': student.social_science_score if student.social_science_score is not None else 5.0,
                'arts_score': student.arts_score if student.arts_score is not None else 5.0,
                'score_c': test_answer.score_c,
                'score_h': test_answer.score_h,
                'score_a': test_answer.score_a,
                'score_s': test_answer.score_s,
                'score_i': test_answer.score_i,
                'score_d': test_answer.score_d,
                'score_e': test_answer.score_e,
                'student_id': student.id
            }
            
            training_data.append(student_data)
            labels.append(rec.career_id)
        
        if len(training_data) < 5:
            print(f"No hay suficientes datos de entrenamiento. Se necesitan al menos 5 ejemplos. Actuales: {len(training_data)}")
            return False
        
        # Convertir a DataFrame
        X = pd.DataFrame(training_data)
        student_profiles = X.copy()  # Guardar copia con IDs para KNN
        
        # Eliminar columna de ID para entrenamiento
        if 'student_id' in X.columns:
            X = X.drop('student_id', axis=1)
        
        y = np.array(labels)
        
        # Crear y entrenar ensemble de modelos
        recommender = EnsembleRecommender()
        recommender.train_models(X, y, student_profiles)
        
        # Guardar modelos entrenados
        models_dir = os.environ.get('ML_MODELS_DIR', 'app/ml_models/saved_models')
        os.makedirs(models_dir, exist_ok=True)
        recommender.save_models(models_dir)
        
        print("Modelos entrenados y guardados exitosamente.")
        return True

if __name__ == "__main__":
    train_models()