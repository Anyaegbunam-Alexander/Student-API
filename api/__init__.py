from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from api.utils import db
from api.models.models import Teacher, Student, Grade, Course, Admin
from api.students.routes import student_namespace
from api.teahcers.routes import teacher_namespace
from api.courses.routes import course_namespace
from api.auth.auth import auth_namespace
from api.config.config import config_dict


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)

    authorizations = {
        "Bearer Auth" : {
            'type' : "apiKey",
            "in" : "header",
            "name" : 'Authorization',
            "description" : "add a JWT with ** Bearer &lt;JWT&gt; to authorize"
        }
    }
    api = Api(app,
          title="Student API",
          description="A REST API for a student management system (AltSchool 3rd semester project)",
          authorizations=authorizations,
          security="Bearer Auth"
    )

    db.init_app(app)
    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    
    api.add_namespace(student_namespace, path='/students')
    api.add_namespace(teacher_namespace, path='/teachers')
    api.add_namespace(course_namespace, path='/courses')
    api.add_namespace(auth_namespace, path='/auth')

    @app.shell_context_processor
    def make_shell_context():
        return{
            'db':db,
            'Student' : Student,
            'Teacher' : Teacher,
            'Course' : Course,
            'Grade' : Grade,
            'Admin' : Admin
    }


    return app
