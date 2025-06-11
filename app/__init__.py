from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Registrar blueprints con manejo de errores
    try:
        from app.routes import auth
        app.register_blueprint(auth.bp)
        print("✓ Blueprint auth registrado")
    except Exception as e:
        print(f"✗ Error registrando blueprint auth: {e}")
    
    try:
        from app.routes import main
        app.register_blueprint(main.bp)
        print("✓ Blueprint main registrado")
    except Exception as e:
        print(f"✗ Error registrando blueprint main: {e}")
    
    try:
        from app.routes import test
        app.register_blueprint(test.bp)
        print("✓ Blueprint test registrado")
    except Exception as e:
        print(f"✗ Error registrando blueprint test: {e}")
    
    # Importar modelos para que SQLAlchemy los reconozca
    try:
        from app.models import user, student, faculty, career, test_answer, recommendation
        print("✓ Modelos importados correctamente")
    except Exception as e:
        print(f"✗ Error importando modelos: {e}")
    
    return app