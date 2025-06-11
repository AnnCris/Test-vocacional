from app import create_app, db
from app.models.user import User
from app.models.student import Student
from app.models.faculty import Faculty
from app.models.career import Career, Aptitude
from app.models.test_answer import TestAnswer
from app.models.recommendation import Recommendation

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Student': Student,
        'Career': Career,
        'Faculty': Faculty,
        'TestAnswer': TestAnswer,
        'Recommendation': Recommendation,
        'Aptitude': Aptitude
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)