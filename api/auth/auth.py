import validators
from http import HTTPStatus
from flask_restx import Namespace, Resource, fields, abort
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash


from api.auth.oauth import create_access_token_admin, create_access_token_non_admin, token_required
from api.models.models import Admin, Student


auth_namespace = Namespace('auth', description='authentication namespace')


admin_model_input = auth_namespace.model(
    'RegisterAdmin', #check here if error on register
    {
        'email' : fields.String(required=True, description='An email for admin'),
        'password' : fields.String(required=True, description='A password for admin'),
    }
)

admin_model_output = auth_namespace.model(
    'Admin',
    {
        'id' : fields.Integer(),
        'email' : fields.String(),
        'created_at' : fields.DateTime(),
    }

)

login_model = auth_namespace.model(
    'Login',
    {
        'email' : fields.String(required=True, description='An email'),
        'password' : fields.String(required=True, description='A password')
    }
)


admin_model_output_tokens = auth_namespace.model(
    'Admin',
    {
        'email' : fields.String(),
        'access' : fields.String(),
        'token_type' : fields.String(),
        'is_administrator' : fields.Boolean()
    }
)

student_model_output_tokens = auth_namespace.model(
    'Student',
    {
        'email' : fields.String(),
        'access' : fields.String(),
        'token_type' : fields.String(),
        'is_administrator' : fields.Boolean()
    }
)


@auth_namespace.route('/admin/register')
class Admins(Resource):

    @token_required
    @auth_namespace.expect(admin_model_input)
    @auth_namespace.marshal_with(admin_model_output)
    def post(self, payload_dict):
        ''' Create an admin '''
        is_administrator = payload_dict.get('is_administrator')

        if not is_administrator:
            abort(401, 'Not Authorized')

        '''Create an admin'''
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if len(password) < 6:
            abort(400, 'Password is too short')
        
        if not validators.email(email):
            abort(400, 'Email is not valid')

        if Admin.query.filter_by(email=email).first() is not None:
            abort(409, 'Email is taken')

        password_hash = generate_password_hash(password)

        new_admin = Admin(email=email, password=password_hash) 
        new_admin.save()

        return new_admin, HTTPStatus.CREATED


@auth_namespace.route('/admin/login')
class Admins(Resource):

    @auth_namespace.expect(login_model)
    @auth_namespace.marshal_with(admin_model_output_tokens) 
    def post(self):
        ''' Login in and generate jwt for admins '''
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        admin = Admin.query.filter_by(email=email).first()

        if admin and check_password_hash(admin.password, password):
            create_access_token_admin(admin)

            return admin, HTTPStatus.OK
        
        abort(401, 'Wrong credentials')



@auth_namespace.route('/students/login')
class Admins(Resource):

    @auth_namespace.expect(login_model)
    @auth_namespace.marshal_with(student_model_output_tokens) 
    def post(self):
        ''' Login in and generate jwt for students '''
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        student = Student.query.filter_by(email=email).first()

        if student and check_password_hash(student.password, password):
            create_access_token_non_admin(student)

            return student, HTTPStatus.OK
        
        abort(401, 'Wrong credentials')


@auth_namespace.route('/admin/test')
class Admins(Resource):

    @token_required
    def post(self, payload_dict):
        ''' Test '''
        is_administrator = payload_dict.get('is_administrator')

        return is_administrator, HTTPStatus.OK
        
    