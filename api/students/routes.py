import validators
from http import HTTPStatus
from flask_restx import Namespace, Resource, fields, abort
from flask import request
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.utils import db
from api.auth.oauth import admin_required
from api.models.models import Student, Course, Grade
from api.utils.helpers import calculate_grade, get_grade, grade_scale

student_namespace = Namespace('Students', description='students namespace')

grade_model_output = student_namespace.model(
    'Grade',
    {
        'course' : fields.String(),
        'score': fields.Float(),
        'grade': fields.String()
    }
)

student_model_output = student_namespace.model(
    'Student',
    {
        'id':fields.Integer(),
        'name':fields.String(),
        'email':fields.String(),
        'date_added':fields.DateTime(),
        'GPA' : fields.Float(),
        'student_grades': fields.List(fields.Nested(grade_model_output))
    }
)

student_model_input = student_namespace.model(
    'Student',
    {
        'students' : fields.List(fields.Nested(student_namespace.model('Student', {       
                'name':fields.String(),
                'email':fields.String(),
                'password' : fields.String(),
                'courses': fields.List(fields.Nested(student_namespace.model('Course', {
                    'id': fields.Integer(),
                    'course_grades': fields.Float()
                })))
        })))
    }
)

single_student_model_input = student_namespace.model(
    'Student',
    {    
            'name':fields.String(),
            'email':fields.String(),
            'password' : fields.String(),
            'courses': fields.List(fields.Nested(student_namespace.model('Course', {
                'id': fields.Integer(),
                'course_grades': fields.Float()
            })))
        })


student_model_input_remove_courses = student_namespace.model(
    'StudentCourses',
    {
        'courses': fields.List(fields.Integer(), required=True)
    }
)

@student_namespace.route('/admin/students')
class Students(Resource):

    @admin_required
    @student_namespace.marshal_list_with(student_model_output, envelope='students')
    @student_namespace.doc(
        description = "Get all students (Admin only)")
    def get(self):
        '''Get all students'''

        students = Student.query.all()
        for student in students:
            calculate_grade(student, Course)
        return students, HTTPStatus.OK

    @admin_required
    @student_namespace.marshal_list_with(student_model_output, envelope='student')
    @student_namespace.expect(student_model_input)
    @student_namespace.doc(
        description = "Create new students")
    def post(self):
        '''Create new student(s)'''

        students_to_return = []

        data = request.get_json()
        students = data.get('students')

        for student in students:
            name = student.get('name')
            email = student.get('email')
            password = student.get('password')

            if len(password) < 6:
                abort(HTTPStatus.BAD_REQUEST, 'Password is too short')
            
            if not validators.email(email):
                abort(HTTPStatus.BAD_REQUEST, 'Email is not valid')

            if Student.query.filter_by(email=email).first() is not None:
                abort(HTTPStatus.CONFLICT, 'Email is taken')

            password_hash = generate_password_hash(password)

            new_student = Student(name=name, email=email, password=password_hash)
            new_student.save()
            students_to_return.append(new_student)

        return students_to_return, HTTPStatus.CREATED


@student_namespace.route('/admin/student/<int:id>')
class Students(Resource):

    @admin_required
    @student_namespace.marshal_list_with(student_model_output, envelope='student')
    @student_namespace.doc(
        description = "Get any student by id. (Admin only)")
    def get(self, id):
        '''Get a student by id'''

        student = Student.query.get_or_404(id)

        calculate_grade(student, Course)
                
        return student, HTTPStatus.OK

    @admin_required
    @student_namespace.marshal_list_with(student_model_output, envelope='student')
    @student_namespace.expect(single_student_model_input)
    @student_namespace.doc(
        description = "Update a student by id.")
    def put(self, id):
        '''  Update a student by id'''

        student_to_update = Student.query.get_or_404(id)
        data = request.get_json()
        courses = data.get('courses')
        student_to_update.name = data.get('name')
        student_to_update.email = data.get('email')
        
        if not validators.email(student_to_update.email):
                abort(HTTPStatus.BAD_REQUEST, 'Email is not valid')

        if courses:
            for course in courses:
                course_id = course.get('id')
                score = course.get('score')
                course_obj = Course.query.filter_by(id=course_id).first()

                if course_obj:
                    if course_obj in student_to_update.student_courses:
                        pass
                    else:
                        student_to_update.student_courses.append(course_obj)
                
                    queried_grade = Grade.query.filter_by(student_id=id, course_id=course_id).first()
                    if queried_grade:
                        queried_grade.score = score
                    else:
                        grade_obj = Grade(student_id=student_to_update.id, course_id=course_obj.id, score=score)
                        db.session.add(grade_obj)

        db.session.commit()
        calculate_grade(student_to_update, Course)

        return student_to_update, HTTPStatus.OK

    @admin_required
    @student_namespace.doc(
        description = "Delete a student by id.")
    def delete(self, id):
        '''Delete a student by id'''

        student_to_delete = Student.query.get_or_404(id)
        student_to_delete.delete()
        return "", HTTPStatus.NO_CONTENT


@student_namespace.route('/admin/student/remove-course/<int:id>')
class Students(Resource):
    @admin_required
    @student_namespace.marshal_with(student_model_output, envelope='student')
    @student_namespace.expect(student_model_input_remove_courses)
    @student_namespace.doc(
        description = "Remove/Unregster courses the student is enrolled in using the student id and course ids (Admin only)")
    def put(self, id):
        '''Remove/Unregister courses a student is enrolled in'''

        student_to_update = Student.query.get_or_404(id)
        data = request.get_json()
        courses = data.get('courses')

        # Add each course from the list obtained from the request to the student's list of courses
        if courses:
            for course_id in courses:
                course_obj = Course.query.get_or_404(course_id)

                # Remove the course to the student's list of courses
                
                if course_obj:
                    if course_obj in student_to_update.student_courses:
                        student_to_update.student_courses.remove(course_obj)
                
                    queried_grade = Grade.query.filter_by(student_id=id, course_id=course_id).first()
                    if queried_grade:
                        db.session.delete(queried_grade)

        db.session.commit()
        calculate_grade(student_to_update, Course)


        return student_to_update, HTTPStatus.OK


@student_namespace.route('/student/<int:id>')
class Students(Resource):

    @jwt_required()
    @student_namespace.marshal_list_with(student_model_output, code=200, envelope='student')
    @student_namespace.doc(
        description = "The student can get their own details only by their id.")
    def get(self, id):
        ''' Get a student by id (the registered student)'''
        
        query_id = get_jwt_identity()
        if query_id != id:
            abort(HTTPStatus.UNAUTHORIZED, "You are not authorized!")
        student = Student.query.get_or_404(id)
    

        total_quality_points = 0
        total_course_units = 0

        for item in student.student_grades:
            item.grade = get_grade(item.score)
            course_units = Course.query.get_or_404(item.course_id).units
            quality_points = course_units * grade_scale.get(item.grade)
            total_quality_points = total_quality_points + quality_points
            item.course = item.grade_course
            total_course_units = total_course_units + course_units
        
        if total_course_units and total_quality_points:
                        student.GPA = round((total_quality_points/total_course_units), 2)            
        
        return student, HTTPStatus.OK