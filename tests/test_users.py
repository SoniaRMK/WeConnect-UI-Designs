import unittest
import json
from resources import app, db
# from run import UserRegister, UserLogin
# from models.models import User
from flask_testing import TestCase


class BaseTestCase(TestCase):
    """Base test case to test the API"""

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:brian@localhost/dbtests'
        return app

    def setUp(self):
        db.create_all()
        self.user = {
            "user_email" : "soniakddd@gmail.com",
            "user_password" : "1234567890"
        }

    def register(self):
        tester = app.test_client(self)
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.user),
                                   content_type="application/json")
        return response

    def login(self):
        user = {"username": 'martin', "password": "banana"}
        response = self.client.post("/api/v2/login", data=json.dumps(user), content_type="application/json")
        return response
        # db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
class TestUserRegister(unittest.TestCase):

    # def setUp(self):
    #     self.app=app.test_client()
    #     db.session.remove()
    #     db.drop_all()
    #     db.create_all()
        

    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()

    def test_register_user_success(self):
        """Ensures that a user is registered successfully"""
        response = self.app.post('/api/v2/auth/register', content_type='application/json', 
                            data=json.dumps(self.user))
        self.assertEqual(response.status_code, 201)

    def test_register_user_already_exists(self):
        """Ensures that a user is not registered twice"""
        response = self.app.post('/api/v2/auth/register', content_type='application/json', data=json.dumps(self.user))
        response = self.app.post('/api/v2/auth/register', content_type='application/json', data=json.dumps(self.user))
        self.assertEqual(response.status_code, 409)

    def test_register_user_missing_credential(self):
        """Ensures that a user is not registered with missing credential"""
        response = self.app.post('/api/v2/auth/register', content_type='application/json',
                            data=json.dumps({"user_email": "afgc@yyyy.zzz"}))
        self.assertEqual(response.status_code, 400)

    def test_user_login_success(self):
        """Ensures that a user logs on successfully"""
        login = self.app.post('/api/v2/auth/login', content_type='application/json',
                            data=json.dumps(self.user))
        self.assertEqual(login.status_code, 200)

    def test_user_login_fail(self):
        """Ensures that a user can't log on with missing credential"""
        response = self.app.post('/api/v2/auth/login', content_type='application/json',
                            data=json.dumps({"userEmail": "soniaddd@gmail.com", "userPassword": ""}))
        self.assertEqual(response.status_code, 400)

    def test_login_wrong_credentials(self):
        """Ensures that a user can't log on with wrong credentials"""
        response = self.app.post('/api/v2/auth/login', content_type='application/json',
                            data=json.dumps({"userEmail": "soniakddd@gmail.com", "userPassword": "67kK0"}))
        self.assertEqual(response.status_code, 400)

    def test_user_logout_token_required(self):
        """Ensures that a user can't log out without a token"""
        response = self.app.post('/api/v2/auth/logout', content_type='application/json',
                            data=json.dumps(self.user))
        self.assertEqual(response.status_code, 401)
       
if __name__ == "__main__":
    unittest.main()