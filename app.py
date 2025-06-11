# app.py
from app import create_app, db
from flask_session import Session

app = create_app()

# Configurar Flask-Session
Session(app)

if __name__ == '__main__':
    app.run(debug=True)