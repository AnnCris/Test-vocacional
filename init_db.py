#!/usr/bin/env python3
"""
Script para inicializar la base de datos PostgreSQL del sistema de recomendación de carreras
Compatible con SQLAlchemy 2.x
"""

from app import create_app, db
from app.models.user import User
from app.models.student import Student
from app.models.faculty import Faculty
from app.models.career import Career, Aptitude
from app.models.test_answer import TestAnswer
from app.models.recommendation import Recommendation
import os
import sys
from sqlalchemy import text

def check_database_connection():
    """Verifica la conexión a la base de datos PostgreSQL"""
    try:
        app = create_app()
        with app.app_context():
            # Usar la nueva sintaxis de SQLAlchemy 2.x
            result = db.session.execute(text('SELECT 1'))
            result.fetchone()
            print("✓ Conexión a PostgreSQL exitosa")
            return True
    except Exception as e:
        print(f"✗ Error conectando a PostgreSQL: {e}")
        print("\nVerifica que:")
        print("1. PostgreSQL esté ejecutándose")
        print("2. La base de datos 'test_vocacional' exista")
        print("3. Las credenciales en config.py sean correctas")
        print("4. La versión de SQLAlchemy sea compatible")
        return False

def create_database_if_not_exists():
    """Crea la base de datos si no existe"""
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    
    try:
        # Conectar sin especificar base de datos
        conn = psycopg2.connect(
            host="localhost",
            user="postgres", 
            password="2458"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'test_vocacional'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute('CREATE DATABASE test_vocacional')
            print("✓ Base de datos 'test_vocacional' creada")
        else:
            print("✓ Base de datos 'test_vocacional' ya existe")
            
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Error creando base de datos: {e}")
        return False

def check_sqlalchemy_version():
    """Verifica la versión de SQLAlchemy"""
    try:
        import sqlalchemy
        version = sqlalchemy.__version__
        print(f"✓ SQLAlchemy versión: {version}")
        
        # Comprobar si es versión 2.x
        major_version = int(version.split('.')[0])
        if major_version >= 2:
            print("✓ Usando SQLAlchemy 2.x (sintaxis moderna)")
            return True
        else:
            print("⚠ Usando SQLAlchemy 1.x (sintaxis legacy)")
            return False
            
    except Exception as e:
        print(f"✗ Error verificando SQLAlchemy: {e}")
        return False

def init_database():
    """Inicializa la base de datos y crea las tablas"""
    print("Iniciando configuración de la base de datos PostgreSQL...")
    
    # Verificar versión de SQLAlchemy
    is_sqlalchemy_2x = check_sqlalchemy_version()
    
    # Crear base de datos si no existe
    if not create_database_if_not_exists():
        return False
    
    # Verificar conexión
    if not check_database_connection():
        return False
    
    app = create_app()
    
    with app.app_context():
        try:
            # Eliminar todas las tablas existentes (cuidado en producción!)
            db.drop_all()
            print("✓ Tablas existentes eliminadas")
            
            # Crear todas las tablas
            db.create_all()
            print("✓ Tablas creadas exitosamente")
            
            # Verificar que las tablas se crearon
            if is_sqlalchemy_2x:
                # SQLAlchemy 2.x
                inspector_query = text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                result = db.session.execute(inspector_query)
                tables = [row[0] for row in result.fetchall()]
            else:
                # SQLAlchemy 1.x (fallback)
                tables = db.engine.table_names()
            
            expected_tables = ['users', 'students', 'faculties', 'careers', 'test_answers', 'recommendations']
            missing_tables = [table for table in expected_tables if table not in tables]
            
            if missing_tables:
                print(f"⚠ Faltan tablas: {missing_tables}")
            else:
                print("✓ Todas las tablas fueron creadas correctamente")
            
            # Crear facultades de ejemplo para universidades bolivianas
            create_sample_faculties()
            
            # Crear carreras de ejemplo
            create_sample_careers()
            
            # Crear usuario administrador de prueba
            create_admin_user()
            
            print("✓ Base de datos inicializada correctamente")
            return True
            
        except Exception as e:
            print(f"✗ Error inicializando base de datos: {e}")
            import traceback
            print("Detalles del error:")
            traceback.print_exc()
            return False

def create_admin_user():
    """Crea un usuario administrador de prueba"""
    try:
        admin = User.query.filter_by(email='admin@test.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@test.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.flush()  # Para obtener el ID
            
            # Crear perfil de estudiante para el admin
            student = Student(
                user_id=admin.id,
                first_name='Administrador',
                last_name='Sistema',
                grade='6to de secundaria',
                school='Sistema de Prueba',
                # Calificaciones de ejemplo (sistema boliviano 1-100)
                matematicas_score=85,
                fisica_score=80,
                quimica_score=82,
                biologia_score=78,
                lenguaje_score=88,
                ingles_score=75,
                ciencias_sociales_score=85,
                filosofia_score=80,
                valores_score=90,
                artes_plasticas_score=70,
                educacion_musical_score=65,
                educacion_fisica_score=85
            )
            db.session.add(student)
            
            db.session.commit()
            print("✓ Usuario administrador creado (admin@test.com / admin123)")
        else:
            print("✓ Usuario administrador ya existe")
            
    except Exception as e:
        print(f"✗ Error creando usuario admin: {e}")
        db.session.rollback()

def create_sample_faculties():
    """Crea facultades de ejemplo basadas en universidades bolivianas"""
    faculties_data = [
        {
            'name': 'Facultad de Ingeniería',
            'description': 'Facultad dedicada a las ciencias de la ingeniería y tecnología'
        },
        {
            'name': 'Facultad de Medicina',
            'description': 'Facultad de ciencias médicas y de la salud'
        },
        {
            'name': 'Facultad de Ciencias Económicas y Financieras',
            'description': 'Facultad dedicada a ciencias económicas, administrativas y financieras'
        },
        {
            'name': 'Facultad de Humanidades y Ciencias de la Educación',
            'description': 'Facultad de humanidades, educación y ciencias sociales'
        },
        {
            'name': 'Facultad de Derecho y Ciencias Políticas',
            'description': 'Facultad de ciencias jurídicas y políticas'
        },
        {
            'name': 'Facultad de Ciencias Puras y Naturales',
            'description': 'Facultad de ciencias exactas y naturales'
        },
        {
            'name': 'Facultad de Arquitectura y Artes',
            'description': 'Facultad de arquitectura, artes y diseño'
        },
        {
            'name': 'Facultad de Agronomía',
            'description': 'Facultad de ciencias agropecuarias y forestales'
        }
    ]
    
    try:
        for faculty_data in faculties_data:
            existing = Faculty.query.filter_by(name=faculty_data['name']).first()
            if not existing:
                faculty = Faculty(**faculty_data)
                db.session.add(faculty)
        
        db.session.commit()
        print("✓ Facultades creadas")
        
    except Exception as e:
        print(f"✗ Error creando facultades: {e}")
        db.session.rollback()

def create_sample_careers():
    """Crea carreras de ejemplo del sistema universitario boliviano"""
    careers_data = [
        # Ingeniería
        {'name': 'Ingeniería de Sistemas', 'faculty_name': 'Facultad de Ingeniería', 
         'description': 'Carrera enfocada en el desarrollo de sistemas informáticos y tecnología',
         'areas': {'i': 0.9, 'e': 0.7, 'c': 0.4}},
        
        {'name': 'Ingeniería Civil', 'faculty_name': 'Facultad de Ingeniería',
         'description': 'Carrera dedicada a la construcción de infraestructura y obras civiles',
         'areas': {'i': 0.8, 'e': 0.6, 'd': 0.3}},
        
        {'name': 'Ingeniería Industrial', 'faculty_name': 'Facultad de Ingeniería',
         'description': 'Optimización de procesos industriales y productivos',
         'areas': {'i': 0.7, 'c': 0.6, 'e': 0.5}},
        
        # Medicina
        {'name': 'Medicina', 'faculty_name': 'Facultad de Medicina',
         'description': 'Carrera para formar médicos generales con conocimiento integral',
         'areas': {'s': 0.9, 'e': 0.6, 'h': 0.4}},
        
        {'name': 'Enfermería', 'faculty_name': 'Facultad de Medicina',
         'description': 'Cuidado integral del paciente y atención en salud',
         'areas': {'s': 0.8, 'h': 0.5, 'c': 0.3}},
        
        # Economía
        {'name': 'Administración de Empresas', 'faculty_name': 'Facultad de Ciencias Económicas y Financieras',
         'description': 'Gestión y administración de organizaciones empresariales',
         'areas': {'c': 0.9, 'h': 0.4, 'i': 0.3}},
        
        {'name': 'Contaduría Pública', 'faculty_name': 'Facultad de Ciencias Económicas y Financieras',
         'description': 'Gestión contable, financiera y auditoría empresarial',
         'areas': {'c': 0.8, 'e': 0.4, 'h': 0.3}},
        
        # Humanidades
        {'name': 'Psicología', 'faculty_name': 'Facultad de Humanidades y Ciencias de la Educación',
         'description': 'Estudio del comportamiento humano y procesos mentales',
         'areas': {'h': 0.8, 's': 0.6, 'a': 0.3}},
        
        {'name': 'Comunicación Social', 'faculty_name': 'Facultad de Humanidades y Ciencias de la Educación',
         'description': 'Comunicación, periodismo y medios de información',
         'areas': {'h': 0.7, 'a': 0.6, 'c': 0.4}},
        
        # Derecho
        {'name': 'Derecho', 'faculty_name': 'Facultad de Derecho y Ciencias Políticas',
         'description': 'Ciencias jurídicas, legales y administración de justicia',
         'areas': {'h': 0.8, 'd': 0.5, 'c': 0.4}},
        
        # Ciencias
        {'name': 'Biología', 'faculty_name': 'Facultad de Ciencias Puras y Naturales',
         'description': 'Estudio de los seres vivos y procesos biológicos',
         'areas': {'e': 0.9, 's': 0.5, 'h': 0.3}},
        
        {'name': 'Química', 'faculty_name': 'Facultad de Ciencias Puras y Naturales',
         'description': 'Estudio de la materia, sus transformaciones y propiedades',
         'areas': {'e': 0.8, 'i': 0.4, 's': 0.3}},
        
        # Arquitectura y Artes
        {'name': 'Arquitectura', 'faculty_name': 'Facultad de Arquitectura y Artes',
         'description': 'Diseño y construcción de espacios habitables',
         'areas': {'a': 0.8, 'i': 0.6, 'h': 0.3}},
        
        {'name': 'Diseño Gráfico', 'faculty_name': 'Facultad de Arquitectura y Artes',
         'description': 'Comunicación visual, diseño y artes gráficas',
         'areas': {'a': 0.9, 'i': 0.4, 'c': 0.3}},
        
        # Agronomía
        {'name': 'Ingeniería Agronómica', 'faculty_name': 'Facultad de Agronomía',
         'description': 'Producción agropecuaria, desarrollo rural y manejo de recursos naturales',
         'areas': {'e': 0.7, 'i': 0.5, 'c': 0.4}}
    ]
    
    try:
        for career_data in careers_data:
            faculty = Faculty.query.filter_by(name=career_data['faculty_name']).first()
            if not faculty:
                continue
                
            existing = Career.query.filter_by(name=career_data['name']).first()
            if not existing:
                career = Career(
                    name=career_data['name'],
                    description=career_data['description'],
                    faculty_id=faculty.id,
                    area_c=career_data['areas'].get('c', 0.0),
                    area_h=career_data['areas'].get('h', 0.0),
                    area_a=career_data['areas'].get('a', 0.0),
                    area_s=career_data['areas'].get('s', 0.0),
                    area_i=career_data['areas'].get('i', 0.0),
                    area_d=career_data['areas'].get('d', 0.0),
                    area_e=career_data['areas'].get('e', 0.0)
                )
                db.session.add(career)
        
        db.session.commit()
        print("✓ Carreras creadas")
        
    except Exception as e:
        print(f"✗ Error creando carreras: {e}")
        db.session.rollback()

if __name__ == '__main__':
    print("=== Inicialización de Base de Datos PostgreSQL ===\n")
    
    # Verificar que psycopg2 esté instalado
    try:
        import psycopg2
    except ImportError:
        print("✗ Error: psycopg2 no está instalado.")
        print("Instálalo con: pip install psycopg2-binary")
        sys.exit(1)
    
    success = init_database()
    
    if success:
        print("\n=== ¡Inicialización Completada! ===")
        print("Puedes iniciar la aplicación con: python app.py")
        print("\nDatos de prueba:")
        print("- Usuario admin: admin@test.com / admin123")
        print("- Base de datos: test_vocacional")
        print("- Facultades: 8 facultades creadas")
        print("- Carreras: 16 carreras de ejemplo")
    else:
        print("\n=== Error en la Inicialización ===")
        print("Revisa los mensajes de error arriba y corrige antes de continuar.")
        sys.exit(1)