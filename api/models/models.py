from api.utils import db
from datetime import datetime


class Teacher(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)
    teacher_courses = db.relationship('Course', backref=db.backref('teacher', lazy=True), overlaps="teacher,teacher_courses")

    def __repr__(self) -> str:
        return self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Grade(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    score = db.Column(db.Float())
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id'), nullable=False)
    grade_student = db.relationship('Student', backref=db.backref('students', lazy=True))
    grade_course = db.relationship('Course', backref=db.backref('courses', lazy=True))
    course_id = db.Column(db.Integer(), db.ForeignKey('course.id'), nullable=False, info={'parent_class': 'Course'})
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id'),)

    def __repr__(self) -> str:
        ...

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    

class Course(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    units = db.Column(db.Integer())
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)
    teacher_id = db.Column(db.Integer(), db.ForeignKey('teacher.id'), nullable=True)
    course_teacher = db.relationship('Teacher', backref=db.backref('courses', lazy=True), overlaps="teacher,teacher_courses")
    course_students = db.relationship('Student', secondary='student_courses', back_populates='student_courses')
    course_grades = db.relationship('Grade', backref=db.backref('grades_course', lazy=True))


    def __repr__(self) -> str:
        return self.title
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

class Student(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)
    student_courses = db.relationship('Course', secondary='student_courses', back_populates='course_students')
    student_grades = db.relationship('Grade', backref=db.backref('grades_student', lazy=True))

    def __repr__(self) -> str:
        return self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

student_courses = db.Table('student_courses',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)
    

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return self.email
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
