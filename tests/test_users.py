import unittest
import json
from resources import app, api, db
from run import UserRegister, UserLogin


class TestUser(unittest.TestCase):
    """Tests for the user api i.e. user registration, login, logout and password resetting"""

    def create_app(self):
        """Creates the app for testing"""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost/testdb'
        return app
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        db.session.remove()
        db.drop_all()
        db.create_all()
        self.user = {'user_email' : 'soniak@gmail.com', 'user_password' : 'qWerty123'}

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_user_success(self):
        """Ensures that a user is registered successfully"""
        response = self.app.post('/api/v2/auth/register', content_type='application/json',
                            data=json.dumps({'user_email': 'aklod@gmail.com', 'user_password': 'qouyWerty123'}))
        self.assertEqual(response.status_code, 201)

    def test_register_user_exists(self):
        """Ensures that a user is not registered twice"""
        response = self.app.post('/api/v2/auth/register', content_type='application/json',
                            data=json.dumps(self.user))
        response = self.app.post('/api/v2/auth/register', content_type='application/json',
                            data=json.dumps(self.user))
        self.assertEqual(response.status_code, 409)

    def test_register_user_fail(self):
        """Ensures that a user is not registered with missing credential"""
        response = self.app.post('/api/v2/auth/register', content_type='application/json', 
                        data=json.dumps({"user_email": "afgc@yyyy.zzz"}))
        self.assertEqual(response.status_code, 400)

    def test_user_login_success(self):
        """Ensures that a user logs on successfully"""
        response = self.app.post('/api/v2/auth/register', content_type='application/json', data=json.dumps(self.user))
        login = self.app.post('/api/v2/auth/login', content_type='application/json', data=json.dumps(self.user))
        self.assertEqual(login.status_code, 200)

    def test_user_login_fail(self):
        """Ensures that a user can't log on when not registered"""
        response = self.app.post('/api/v2/auth/register', content_type='application/json', data=json.dumps(self.user))
        response = self.app.post('/api/v2/auth/login', content_type='application/json', 
                        data=json.dumps({"user_email": "soniak1234@gmail.com", "user_password": ""}))
        self.assertEqual(response.status_code, 401)

    def test_login_wrong_credentials(self):
        """Ensures that a user can't log on with wrong credentials"""
        response = self.app.post('/api/v2/auth/register', content_type='application/json', data=json.dumps(self.user))
        response = self.app.post('/api/v2/auth/login', content_type='application/json', 
                        data=json.dumps({"user_email": "soniakxx@gmail.com", "user_password": "67kK0"}))
        self.assertEqual(response.status_code, 401)

    def tests_user_logout(self):
        """ test a user logs out successfully """
        register = self.app.post('/api/v2/auth/register', content_type='application/json', data=json.dumps(self.user))
        login = self.app.post('/api/v2/auth/login', content_type='application/json', data=json.dumps(self.user))
        login_data = json.loads(login.data.decode())
        access_token = login_data["token"]
        logout = self.app.post('/api/v2/auth/logout', headers={'Authorization': 'Bearer ' + access_token}, 
                        content_type='application/json')
        self.assertEqual(logout.status_code, 200)

    def test_user_reset_password(self):
        """ tests a registered user can reset their password """
        response = self.app.post('/api/v2/auth/register', content_type = 'application/json', data = json.dumps(self.user))
        response = self.app.post('/api/v2/auth/reset-password', content_type = 'application/json',
                    data = json.dumps({'user_email': 'soniak@gmail.com', 'user_password': 'qouyWerty123', 'confirm_password': 'qouyWerty123'}))
        self.assertEqual(response.status_code, 200)

    def test_user_reset_password_fail(self):
        """ tests a non-registered user cannot reset their password """
        response = self.app.post('/api/v2/auth/register', content_type = 'application/json',
                        data = json.dumps(self.user))
        response = self.app.post('/api/v2/auth/reset-password', content_type = 'application/json',
                                data = json.dumps({'user_email': 'karungi@gmail.com', 'user_password': 'qWerty123', 'confirm_password': 'qWerty123'}))
        self.assertEqual(response.status_code, 404)
        
if __name__ == "__main__":
    unittest.main()
