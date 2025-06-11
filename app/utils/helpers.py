import hashlib
import numpy as np
import os
import random
import string
from datetime import datetime, timedelta
import json

def generate_password_hash(password):
    """
    Genera un hash seguro para contraseñas
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        str: Hash de la contraseña
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    password_hash = salt + password_hash
    
    return 'pbkdf2:sha256:150000$' + password_hash.hex()

def check_password_hash(stored_hash, password):
    """
    Verifica si una contraseña coincide con su hash almacenado
    
    Args:
        stored_hash: Hash almacenado
        password: Contraseña a verificar
        
    Returns:
        bool: True si la contraseña coincide, False en caso contrario
    """
    if not stored_hash.startswith('pbkdf2:sha256:150000$'):
        return False
    
    hash_parts = stored_hash.split('$')
    if len(hash_parts) != 2:
        return False
    
    salt = bytes.fromhex(hash_parts[1][:64])
    stored_password = bytes.fromhex(hash_parts[1][64:])
    
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
    return password_hash == stored_password

def generate_secret_key(length=32):
    """
    Genera una clave secreta aleatoria para la aplicación
    
    Args:
        length: Longitud de la clave (por defecto 32)
        
    Returns:
        str: Clave secreta generada
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def format_date(date_obj, format_str='%d/%m/%Y'):
    """
    Formatea un objeto de fecha en una cadena legible
    
    Args:
        date_obj: Objeto datetime
        format_str: Formato de fecha deseado
        
    Returns:
        str: Fecha formateada
    """
    if not date_obj:
        return ""
    
    return date_obj.strftime(format_str)

def calculate_age(birth_date):
    """
    Calcula la edad a partir de la fecha de nacimiento
    
    Args:
        birth_date: Fecha de nacimiento (objeto datetime.date)
        
    Returns:
        int: Edad en años
    """
    if not birth_date:
        return None
    
    today = datetime.now().date()
    age = today.year - birth_date.year
    
    # Ajustar si aún no ha llegado el cumpleaños de este año
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return age

def calculate_compatibility_score(student_scores, career_areas):
    """
    Calcula un puntaje de compatibilidad entre un estudiante y una carrera
    
    Args:
        student_scores: Diccionario con puntajes CHASIDE del estudiante
        career_areas: Diccionario con pesos de áreas CHASIDE para la carrera
        
    Returns:
        float: Puntaje de compatibilidad (0-1)
    """
    total_score = 0.0
    total_weight = 0.0
    
    for area, weight in career_areas.items():
        if area.lower() in student_scores and weight > 0:
            student_score = student_scores[area.lower()]
            total_score += student_score * weight
            total_weight += weight
    
    if total_weight > 0:
        return total_score / total_weight
    
    return 0.0

def sanitize_input(text):
    """
    Elimina caracteres potencialmente peligrosos de una entrada de texto
    
    Args:
        text: Texto a sanitizar
        
    Returns:
        str: Texto sanitizado
    """
    if not text:
        return ""
    
    # Eliminar caracteres de script y SQL injection
    blacklist = ['<script', '</script>', 'SELECT', 'INSERT', 'DELETE', 'UPDATE', 'DROP', '--']
    sanitized = text
    
    for item in blacklist:
        sanitized = sanitized.replace(item, '')
    
    return sanitized

def json_to_pretty_html(json_str):
    """
    Convierte una cadena JSON en HTML con formato para mejor visualización
    
    Args:
        json_str: Cadena JSON
        
    Returns:
        str: HTML formateado
    """
    try:
        parsed = json.loads(json_str)
        pretty_json = json.dumps(parsed, indent=4, sort_keys=True)
        
        # Escapar caracteres HTML
        html_escaped = pretty_json.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Aplicar estilo
        styled_html = f'<pre style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; overflow: auto;">{html_escaped}</pre>'
        
        return styled_html
    except:
        return f'<pre>{json_str}</pre>'