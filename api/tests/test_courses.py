import unittest
from api import create_app
from api.config.config import config_dict
from flask_jwt_extended import create_access_token


from api.utils import db
from api.models.models import Course


class CourseTestCase(unittest.TestCase):

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


    def test_create_course(self):
        token = create_access_token(identity='testadmin', additional_claims={"is_administrator" : True})

        headers = {"Authorization":f"Bearer {token}"}
        
        data = {"courses" : [{
                    "title" : "testcourse"
                }]}


        response = self.client.post('courses/admin/courses', json=data, headers=headers)

        course = Course.query.filter_by(title=data["courses"][0]['title']).first()

        self.assertEqual(course.title, data["courses"][0]['title'])

        self.assertEqual(response.status_code, 201)



    def test_get_all_courses(self):
        token = create_access_token(identity='testadmin', additional_claims={"is_administrator" : True})

        headers = {"Authorization":f"Bearer {token}"}
        

        response = self.client.get('courses/admin/courses', headers=headers)

        course = Course.query.all()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json, {'courses': []})
        
    

    def test_get_one_course(self, id=1):

        token = create_access_token(identity='testadmin', additional_claims={"is_administrator" : True})

        headers = {"Authorization":f"Bearer {token}"}
        
        course = Course(title='testcourse')
        db.session.add(course)
        db.session.commit()

        # get the course object from the database
        course = Course.query.filter_by(title=course.title).first()

        response = self.client.get('courses/admin/course/1', headers=headers)

        self.assertEqual(response.status_code, 200)



