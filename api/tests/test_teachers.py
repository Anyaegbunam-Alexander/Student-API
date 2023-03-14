import unittest
from api import create_app
from api.config.config import config_dict
from flask_jwt_extended import create_access_token
from sqlalchemy.orm import Session


from api.utils import db
from api.models.models import Teacher


class TeacherTestCase(unittest.TestCase):

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


    def test_create_teacher(self):
        token = create_access_token(identity='testadmin', additional_claims={"is_administrator" : True})

        headers = {"Authorization":f"Bearer {token}"}
        
        data = {"teachers" : [{
                    "name" : "testteacher",
                    "email" : "testteacher@email.com"
                }]}


        response = self.client.post('teachers/admin/teachers', json=data, headers=headers)

        teacher = Teacher.query.filter_by(email=data["teachers"][0]['email']).first()

        self.assertEqual(teacher.name, data["teachers"][0]['name'])

        self.assertEqual(response.status_code, 201)



    def test_get_all_teachers(self):
        token = create_access_token(identity='testadmin', additional_claims={"is_administrator" : True})

        headers = {"Authorization":f"Bearer {token}"}
        

        response = self.client.get('teachers/admin/teachers', headers=headers)

        teacher = Teacher.query.all()

        self.assertEqual(response.json, {'teachers': []})

        self.assertEqual(response.status_code, 200)

    

    def test_get_one_teacher(self, id=1):

        token = create_access_token(identity='testadmin', additional_claims={"is_administrator" : True})

        headers = {"Authorization":f"Bearer {token}"}
        
        teacher = Teacher(name='testteacher', email='testemail')
        db.session.add(teacher)
        db.session.commit()

        # get the teacher object from the database
        teacher = Teacher.query.filter_by(email=teacher.email).first()

        response = self.client.get('teachers/admin/teacher/1', headers=headers)

        self.assertEqual(response.status_code, 200)






