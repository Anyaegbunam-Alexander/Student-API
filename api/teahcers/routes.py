from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields, abort

from api.utils import db
from api.models.models import Teacher
from api.auth.oauth import token_required

teacher_namespace = Namespace('teacher', description='teachers namespace')


teacher_model_input = teacher_namespace.model(
    'Teacher',
    {
        'teachers': fields.List(fields.Nested(teacher_namespace.model('Teacher', {
                    'name':fields.String(),
                    'email':fields.String(),
       })))
    }
)


teacher_model_output = teacher_namespace.model(
    'Teacher',
    {
        'id':fields.Integer(),
        'name':fields.String(),
        'email':fields.String(),
        'date_joined' : fields.String(),
        'courses': fields.List(fields.String('course.title'))
    }
)



@teacher_namespace.route('/admin/teachers')
class Teachers(Resource):
    @token_required
    @teacher_namespace.marshal_list_with(teacher_model_output, envelope='teachers')
    def get(self, payload_dict):
        '''Get all teachers'''
        is_administrator = payload_dict.get('is_administrator')

        if not is_administrator:
            abort(HTTPStatus.UNAUTHORIZED, 'Not Authorized')

        teachers = Teacher.query.all()
        return teachers, HTTPStatus.OK


    @token_required
    @teacher_namespace.marshal_list_with(teacher_model_output, envelope='teacher')
    @teacher_namespace.expect(teacher_model_input)
    def post(self, payload_dict):
        '''Create new teacher(s)'''
        is_administrator = payload_dict.get('is_administrator')

        if not is_administrator:
            abort(HTTPStatus.UNAUTHORIZED, 'Not Authorized')

        teachers_to_return = []
        
        
        data = request.get_json()


        teachers = data.get('teachers')
        for teacher in teachers:
            name = teacher.get('name')
            email = teacher.get('email')

            new_teacher = Teacher(name=name, email=email)
            new_teacher.save()

            teachers_to_return.append(new_teacher)

        return teachers_to_return, HTTPStatus.CREATED


@teacher_namespace.route('/admin/teacher/<int:id>')
class Teachers(Resource):

    @token_required
    @teacher_namespace.marshal_list_with(teacher_model_output, envelope='teacher')
    def get(self, id, payload_dict):
        '''Get a teacher by id'''
        teacher = Teacher.query.get_or_404(id)
        payload_id = payload_dict.get('id')
        is_administrator = payload_dict.get('is_administrator')

        if not is_administrator:
            if teacher.id != payload_id: 
                abort(HTTPStatus.UNAUTHORIZED, 'Not Authorized')
            
        return teacher, HTTPStatus.OK
    

    @token_required
    @teacher_namespace.marshal_list_with(teacher_model_output, envelope='teacher')
    @teacher_namespace.expect(teacher_model_input)
    def put(self, id, payload_dict):
        '''Update a teacher by id'''
        is_administrator = payload_dict.get('is_administrator')

        if not is_administrator:
            abort(HTTPStatus.UNAUTHORIZED, 'Not Authorized')

        teacher_to_update = Teacher.query.get_or_404(id)
        data = request.get_json()
        teacher_to_update.name = data.get('name')
        teacher_to_update.email = data.get('email')

        db.session.commit()

        return teacher_to_update, HTTPStatus.OK


    @token_required
    def delete(self, id, payload_dict):
        '''Delete a teacher by id'''
        is_administrator = payload_dict.get('is_administrator')

        if not is_administrator:
            abort(HTTPStatus.UNAUTHORIZED, 'Not Authorized')
            
        teacher_to_delete = Teacher.query.get_or_404(id)
        teacher_to_delete.delete()
        return "", HTTPStatus.NO_CONTENT