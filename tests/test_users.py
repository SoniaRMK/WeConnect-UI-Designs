import sys
sys.path.append('..')
import unittest
import json
from resources import app, api
from run import UserRegister, UserLogin
from resources.user_api import users


class TestUser(unittest.TestCase):
    """Tests for the user api i.e. user registration, login, logout and password resetting"""

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.user = {'userEmail' : 'soniak@gmail.com', 'userPassword' : 'qWerty123'}

    def tearDown(self):
        users.clear()

    def test_register_user_success(self):
        """Ensures that a user is registered successfully"""
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                            data=json.dumps(self.user))
        self.assertEqual(response.status_code, 201)

    def test_register_user_exists(self):
        """Ensures that a user is not registered twice"""
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                            data=json.dumps(self.user))
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                            data=json.dumps(self.user))
        self.assertEqual(response.status_code, 409)

    def test_register_user_fail(self):
        """Ensures that a user is not registered with missing credential"""
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                            data=json.dumps({"userEmail": "afgc@yyyy.zzz"}))
        self.assertEqual(response.status_code, 400)

    def test_user_login_success(self):
        """Ensures that a user logs on successfully"""
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                            data=json.dumps(self.user))
        login = self.app.post('/api/v1/auth/login', content_type='application/json',
                            data=json.dumps(self.user))
        self.assertEqual(login.status_code, 200)

    def test_user_login_fail(self):
        """Ensures that a user can't log on with missing credential"""
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                            data=json.dumps(self.user))
        response = self.app.post('/api/v1/auth/login', content_type='application/json',
                            data=json.dumps({"userEmail": "soniak@gmail.com", "userPassword": ""}))
        self.assertEqual(response.status_code, 401)

    def test_login_wrong_credentials(self):
        """Ensures that a user can't log on with wrong credentials"""
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                            data=json.dumps(self.user))
        response = self.app.post('/api/v1/auth/login', content_type='application/json',
                            data=json.dumps({"userEmail": "soniak@gmail.com", "userPassword": "67kK0"}))
        self.assertEqual(response.status_code, 401)

    def test_user_reset_password(self):
        """ tests a registered user can reset their password """

        response = self.app.post('/api/v1/auth/register', content_type = 'application/json',
                        data = json.dumps(self.user))
        response = self.app.post('/api/v1/auth/reset-password', content_type = 'application/json',
                    data = json.dumps({'userEmail': 'soniak@gmail.com', 'userPassword': 'qouyWerty123'})
                    )
        self.assertEqual(response.status_code, 200)

    def test_user_reset_password_fail(self):
        """ tests a non-registered user cannot reset their password """
        response = self.app.post('/api/v1/auth/register', content_type = 'application/json',
                        data = json.dumps(self.user))
        response = self.app.post('/api/v1/auth/reset-password', content_type = 'application/json',
                    data = json.dumps({'userEmail': 'karungi@gmail.com', 'userPassword': 'qWerty123'})
                    )
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
