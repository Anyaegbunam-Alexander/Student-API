import validators
from http import HTTPStatus
from flask_restx import Namespace, Resource, fields, abort
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token


from api.auth.oauth import admin_required
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



@auth_namespace.route('/admin/admins')
class Admins(Resource):

    @admin_required
    @auth_namespace.marshal_list_with(admin_model_output)
    def get(self):
        '''Get all admins'''
        admins = Admin.query.all()
        return admins, HTTPStatus.OK


@auth_namespace.route('/admin/register')
class Admins(Resource):

    @admin_required
    @auth_namespace.expect(admin_model_input)
    @auth_namespace.marshal_with(admin_model_output)
    def post(self):
        '''Create an admin'''
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if len(password) < 6:
            abort(HTTPStatus.BAD_REQUEST, 'Password is too short')
        
        if not validators.email(email):
            abort(HTTPStatus.BAD_REQUEST, 'Email is not valid')

        if Admin.query.filter_by(email=email).first() is not None:
            abort(HTTPStatus.CONFLICT, 'Email is taken')

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
            
            admin.access = create_access_token(identity=admin.id, additional_claims={"is_administrator" : True})
            admin.is_administrator = True
            admin.token_type = 'bearer'

            return admin, HTTPStatus.OK
        
        abort(HTTPStatus.UNAUTHORIZED, 'Wrong credentials')



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
            student.access = create_access_token(identity=student.id, additional_claims={"is_administrator" : False})
            student.is_administrator = False
            student.token_type = 'bearer'

            return student, HTTPStatus.OK
        
        abort(HTTPStatus.UNAUTHORIZED, 'Wrong credentials')
        
    
@auth_namespace.route('/admin/delete-admin/<int:id>')
class Admins(Resource):

    @admin_required
    def delete(self, id):
        ''' Delete an admin '''
        
        admin_to_delete = Admin.query.get_or_404(id)
        admin_to_delete.delete()

        return "", HTTPStatus.NO_CONTENT
