import validators
from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields, abort

from api.utils import db
from api.models.models import Teacher
from api.auth.oauth import admin_required

teacher_namespace = Namespace('Teacher', description='teachers namespace')


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
    @admin_required
    @teacher_namespace.marshal_list_with(teacher_model_output, envelope='teachers')
    def get(self):
        '''Get all teachers'''
        teachers = Teacher.query.all()
        return teachers, HTTPStatus.OK


    @admin_required
    @teacher_namespace.marshal_list_with(teacher_model_output, envelope='teacher')
    @teacher_namespace.expect(teacher_model_input)
    def post(self):
        '''Create new teacher(s)'''

        teachers_to_return = []
        
        
        data = request.get_json()


        teachers = data.get('teachers')
        for teacher in teachers:
            name = teacher.get('name')
            email = teacher.get('email')

            if not validators.email(email):
                abort(HTTPStatus.BAD_REQUEST, 'Email is not valid')

            new_teacher = Teacher(name=name, email=email)
            new_teacher.save()

            teachers_to_return.append(new_teacher)

        return teachers_to_return, HTTPStatus.CREATED


@teacher_namespace.route('/admin/teacher/<int:id>')
class Teachers(Resource):

    @admin_required
    @teacher_namespace.marshal_list_with(teacher_model_output, envelope='teacher')
    def get(self, id):
        '''Get a teacher by id'''
        teacher = Teacher.query.get_or_404(id)
            
        return teacher, HTTPStatus.OK
    

    @admin_required
    @teacher_namespace.marshal_list_with(teacher_model_output, envelope='teacher')
    @teacher_namespace.expect(teacher_model_input)
    def put(self, id):
        '''Update a teacher by id'''

        teacher_to_update = Teacher.query.get_or_404(id)
        data = request.get_json()
        teacher_to_update.name = data.get('name')
        teacher_to_update.email = data.get('email')

        db.session.commit()

        return teacher_to_update, HTTPStatus.OK


    @admin_required
    def delete(self, id):
        '''Delete a teacher by id'''
            
        teacher_to_delete = Teacher.query.get_or_404(id)
        teacher_to_delete.delete()
        return "", HTTPStatus.NO_CONTENT