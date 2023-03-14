from http import HTTPStatus
from flask_restx import Namespace, Resource, fields
from flask import request

from api.utils import db
from api.auth.oauth import admin_required
from api.models.models import Course

course_namespace = Namespace('Course', description='courses namespace')

course_model_output = course_namespace.model(
    'Course',
    {
        'id':fields.Integer(),
        'title':fields.String(),
        'units':fields.Integer(),
        'teacher':fields.String(attribute='teacher.name'),
        'course_students' : fields.List(fields.String('student.name'))
    }
)


course_model_input = course_namespace.model(
    'Course',
    {
        'courses': fields.List(fields.Nested(course_namespace.model('Course', {
                'title':fields.String(),
                'teacher_id' : fields.Integer(),
                'units' : fields.Integer()
        })))
    }
)


@course_namespace.route('/admin/courses')
class Courses(Resource):

    @admin_required
    @course_namespace.marshal_list_with(course_model_output, envelope='courses')
    def get(self):
        '''Get all courses'''

        courses = Course.query.all()
        return courses, HTTPStatus.OK

    @admin_required
    @course_namespace.marshal_list_with(course_model_output, envelope='courses')
    @course_namespace.expect(course_model_input)
    def post(self):
        '''Create new courses'''
        courses_to_return = []
        
        data = request.get_json()
        courses = data.get('courses')
        for course in courses:
            title = course.get('title')
            teacher_id = course.get('teacher_id')
            units = course.get('units')

            new_course = Course(title=title, teacher_id=teacher_id, units=units)
            new_course.save()
            courses_to_return.append(new_course)

        return courses_to_return, HTTPStatus.CREATED


@course_namespace.route('/admin/course/<int:id>')
class Courses(Resource):
    '''Get a course by id'''
    @admin_required
    @course_namespace.marshal_list_with(course_model_output, envelope='course')
    def get(self, id):
        '''Get a course by id'''
        course = Course.query.get_or_404(id)
        
        return course, HTTPStatus.OK

    @admin_required
    @course_namespace.marshal_with(course_model_output, envelope='course')
    @course_namespace.expect(course_model_input)
    def put(self, id):
        '''Update a course by id'''
            
        course_to_update = Course.query.get_or_404(id)
        data = request.get_json()
        course_to_update.title = data.get('title')
        course_to_update.teacher_id = data.get('teacher_id')
        course_to_update.units = data.get('units')

        db.session.commit()

        return course_to_update, HTTPStatus.OK

    @admin_required
    def delete(self, id):
        '''Delete a course by id'''
        course_to_delete = Course.query.get_or_404(id)
        course_to_delete.delete()

        return "", HTTPStatus.NO_CONTENT