import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-predeterminada'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:2458@localhost/test_vocacional'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuraciones adicionales para la sesión
    SESSION_TYPE = 'filesystem'  # o 'redis', 'memcached', etc. si los tienes disponibles
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_SECURE = False  # Cambiar a True en producción con HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'