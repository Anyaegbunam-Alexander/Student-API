import unittest
from api import create_app
from api.config.config import config_dict
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash


from api.utils import db
from api.models.models import Student


class StudentTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config=config_dict['testing'])
        self.app_contxt = self.app.app_context()
        self.app_contxt.push()
        self.client = self.app.test_client()

        db.create_all()
        


    def tearDown(self):
        db.drop_all()

        self.app_contxt.pop()
        self.app = None
        self.client = None


    def test_create_student(self):
        token = create_access_token(identity='testadmin', additional_claims={"is_administrator" : True})

        headers = {"Authorization":f"Bearer {token}"}
        
        data = {"students" : [{
                    "name" : "teststudent",
                    "email" : "teststudent@email.com",
                    "password" : "testpassword"
                }]}


        response = self.client.post('students/admin/students', json=data, headers=headers)

        student = Student.query.filter_by(email=data["students"][0]['email']).first()

        

        self.assertEqual(student.name, data["students"][0]['name'])
        self.assertEqual(response.status_code, 201)



    def test_student_login(self):

        password = 'testpassword'
        hashed_password = generate_password_hash(password)

        student = Student(name='teststudent', email='teststudent@email.com', password=hashed_password)
        db.session.add(student)
        db.session.commit()

        # get the student object from the database
        student = Student.query.filter_by(email=student.email).first()

        data = {
                    "email" : "teststudent@email.com",
                    "password" : "testpassword"
                }
        
        
        response = self.client.post('auth/students/login', json=data)

        self.assertEqual(response.status_code, 200)


    
    def test_get_all_students(self):
        token = create_access_token(identity='testadmin', additional_claims={"is_administrator" : True})

        headers = {"Authorization":f"Bearer {token}"}
        

        response = self.client.get('students/admin/students', headers=headers)

        student = Student.query.all()


        self.assertEqual(response.json, {'students': []})
        self.assertEqual(response.status_code, 200)

    

    def test_get_one_student(self, id=1):

        token = create_access_token(identity='testadmin', additional_claims={"is_administrator" : True})

        headers = {"Authorization":f"Bearer {token}"}
        
        student = Student(name='teststudent', email='testemail', password='testpassword')
        db.session.add(student)
        db.session.commit()

        # get the student object from the database
        student = Student.query.filter_by(email=student.email).first()

        response = self.client.get('students/admin/student/1', headers=headers)

        self.assertEqual(response.status_code, 200)
        