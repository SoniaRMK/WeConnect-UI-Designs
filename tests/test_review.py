import unittest
import json
from resources import app, db
from run import UserRegister, UserLogin
from models.models import User


class TestUser(unittest.TestCase):

    def setUp(self):
        self.app=app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234567890@localhost/testdb'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_user_success(self):
        """Ensures that a user is registered successfully"""
        response = self.app.post('/api/v2/auth/register',
                            content_type='application/json',
                            data=json.dumps({"user_email": "soniakxxx@yyy.com", "user_password": "jh123"})
                            )
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User registered!', response.data)

    def test_register_user_exists(self):
        """Ensures that a user is not registered twice"""
        response = self.app.post('/api/v2/auth/register',
                            content_type='application/json',
                            data=json.dumps({"user_email": "abc@yyyy.zzz", "user_password": "67890"})
                            )
        self.assertEqual(response.status_code, 409)
        self.assertIn(b'User already exists!', response.data)

    def test_register_user_fail(self):
        """Ensures that a user is not registered with missing credential"""
        response = self.app.post('/api/v2/auth/register',
                            content_type='application/json',
                            data=json.dumps({"user_email": "afgc@yyyy.zzz"})
                            )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Password must be a valid string', response.data)

    def test_user_login_success(self):
        """Ensures that a user logs on successfully"""
        response = self.app.post('/api/v2/auth/login',
                            content_type='application/json',
                            data=json.dumps({"user_email": "abc@yyyy.zzz", "user_password": "67890"})
                            )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in', response.data)

    def test_user_login_fail(self):
        """Ensures that a user can't log on with missing credential"""
        response = self.app.post('/api/v2/auth/login',
                            content_type='application/json',
                            data=json.dumps({"user_email": "abc@yyyy.zzz", "user_password": ""})
                            )
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Password and/or Email are missing!', response.data)

    def test_login_wrong_credentials(self):
        """Ensures that a user can't log on with wrong credentials"""
        response = self.app.post('/api/v2/auth/login',
                            content_type='application/json',
                            data=json.dumps({"user_email": "abc@yyyy.zzz", "user_password": "67kK0"})
                            )
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'User does not Exist!', response.data)
       
if __name__ == "__main__":
    unittest.main()