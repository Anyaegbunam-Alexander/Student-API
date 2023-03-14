import unittest
from api import create_app
from api.config.config import config_dict
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash


from api.utils import db
from api.models.models import Admin


class AdminTestCase(unittest.TestCase):

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


    

    def test_admin_registration(self):

        token = create_access_token(identity='testadmin', additional_claims={"is_administrator" : True})

        headers = {"Authorization":f"Bearer {token}"}
        
        data = {
            "email":"testadmin@company.com",
            "password":"testpassword"
        }


        response = self.client.post('/auth/admin/register', json=data, headers=headers)

        admin = Admin.query.filter_by(email="testadmin@company.com").first()

        self.assertEqual(admin.email, data['email'])

        self.assertEqual(response.status_code, 201)



    
    def test_admin_login(self):

        # create an admin object with a hashed password
        password = 'testpassword'
        hashed_password = generate_password_hash(password)
        admin = Admin(email='testadmin@email.com', password=hashed_password)
        db.session.add(admin)
        db.session.commit()

        # send a POST request to the /auth/admin/login route
        data = {
            "email": admin.email,
            "password": password
        }
        response = self.client.post('/auth/admin/login', json=data)

        self.assertEqual(response.status_code, 200)


    
    def test_get_all_admins(self):
        token = create_access_token(identity='testadmin', additional_claims={"is_administrator" : True})

        headers = {"Authorization":f"Bearer {token}"}
        

        response = self.client.get('auth/admin/admins', headers=headers)

        admin = Admin.query.all()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json, [])