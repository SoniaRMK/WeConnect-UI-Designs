import unittest
import json

from resources import app, db
from run import UserRegister, UserLogin


class TestUser(unittest.TestCase):
    """Tests for the user api i.e. user registration, login, logout and password resetting"""

    def create_app(self):
        """Creates the app for testing"""
        app.config.from_object('config.TestingConfig')
        return app
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        db.session.remove()
        db.drop_all()
        db.create_all()
        self.user = {'user_email' : 'soniak@gmail.com', 'user_name': 'sonjaYXG', 
                    'user_password' : 'qWerty123'}
        self.user_two = {'user_email' : 'karungi@gmail.com', 'user_name': 'Kaynyts000', 
                        'user_password' : 'qWerty123'}

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def get_token(self):
        """ Generate token using details of self.user """
        register = self.app.post('/api/v2/auth/register', 
                            content_type='application/json', 
                            data=json.dumps(self.user))
        login = self.app.post('/api/v2/auth/login', 
                            content_type='application/json', 
                            data=json.dumps(self.user))
        login_data = json.loads(login.data.decode())
        self.access_token = login_data["token"]
        return self.access_token

    def get_token_two(self):
        """ Generate token using details of self.user """
        register = self.app.post('/api/v2/auth/register', 
                                content_type='application/json', 
                                data=json.dumps(self.user_two))
        login = self.app.post('/api/v2/auth/login', 
                                content_type='application/json', 
                                data=json.dumps(self.user_two))
        login_data = json.loads(login.data.decode())
        self.access_token = login_data["token"]
        return self.access_token

    def test_register_user_success(self):
        """Ensures that a user is registered successfully"""
        response = self.app.post('/api/v2/auth/register', 
                            content_type='application/json',
                            data=json.dumps({'user_email': 'aklod@gmail.com', \
                            'user_name': 'Kaynuts000', 'user_password': 'qouyWerty123'}))
        self.assertEqual(response.status_code, 201)

    def test_register_user_missing_username(self):
        """Ensures that a user is registered successfully"""
        response = self.app.post('/api/v2/auth/register', 
                            content_type='application/json',
                            data=json.dumps({'user_email': 'aklod@gmail.com', \
                            'user_name': '', 'user_password': 'qouyWerty123'}))
        self.assertEqual(response.status_code, 403)

    def test_register_user_exists(self):
        """Ensures that a user is not registered twice"""
        response = self.app.post('/api/v2/auth/register', 
                            content_type='application/json',
                            data=json.dumps(self.user))
        response = self.app.post('/api/v2/auth/register', 
                            content_type='application/json',
                            data=json.dumps(self.user))
        self.assertEqual(response.status_code, 409)

    def test_register_user_fail(self):
        """Ensures that a user is not registered with missing password"""
        response = self.app.post('/api/v2/auth/register', 
                        content_type='application/json', 
                        data=json.dumps({"user_email": "afgc@yyyy.zzz", 
                        'user_name': 'Kaynyts000',}))
        self.assertEqual(response.status_code, 400)

    def test_register_user_with_long_email(self):
        """Ensures that a user is not registered with an email longer than 60 characters"""
        response = self.app.post('/api/v2/auth/register', 
                        content_type='application/json', 
                        data=json.dumps({"user_email": "afgchnafgchnafgcafgchnafgchnafgcafgch\
                        nafgchnafgcafgchnafgchnafgcafgchnafgchnafgcafgchnafgchnafgchnafgchna\
                        fgchnafgchnafgchn@yyyy.zzz", 'user_name': 'Kaynyts000',\
                         "user_password":"qwertyhgfn"}))
        self.assertEqual(response.status_code, 403)
    
    def test_register_user_with_spaces_in_password(self):
        """Ensures that a user is not registered with a password having spaces in it"""
        response = self.app.post('/api/v2/auth/register', 
                        content_type='application/json', 
                        data=json.dumps({"user_email": "afgchna@yyyy.zzz", 
                        'user_name': 'Kaynyts000', "user_password":"qwerty hgfn"}))
        self.assertEqual(response.status_code, 403)

    def test_register_user_with_short_password(self):
        """Ensures that a user is not registered with a password having spaces in it"""
        response = self.app.post('/api/v2/auth/register', 
                        content_type='application/json', 
                        data=json.dumps({"user_email": "afgchna@yyyy.zzz",  
                        'user_name': 'Kaynyts000',"user_password":"qwerty"}))
        self.assertEqual(response.status_code, 403)

    def test_register_user_fail_missing_email(self):
        """Ensures that a user is not registered with missing credential"""
        response = self.app.post('/api/v2/auth/register', 
                        content_type='application/json', 
                        data=json.dumps({"user_email": "",  
                        'user_name': 'Kaynyts000',"user_password": "fjkJKNKE3"}))
        self.assertEqual(response.status_code, 403)

    def test_register_user_invalid_email(self):
        """Ensures that a user is not registered with invalid email"""
        response = self.app.post('/api/v2/auth/register', 
                        content_type='application/json', 
                        data=json.dumps({"user_email": "sjhhjfdhjdfhjkfdkjhdf", 
                        'user_name': 'Kaynyts000', "user_password": "fjkJKNKE3"}))
        self.assertEqual(response.status_code, 403)

    def test_user_login_success(self):
        """Ensures that a user logs on successfully"""
        response = self.app.post('/api/v2/auth/register', 
                            content_type='application/json', 
                            data=json.dumps(self.user))
        login = self.app.post('/api/v2/auth/login', 
                            content_type='application/json', 
                            data=json.dumps(self.user))
        self.assertEqual(login.status_code, 200)

    def test_user_login_fail(self):
        """Ensures that a user can't log on when not registered"""
        response = self.app.post('/api/v2/auth/register', 
                            content_type='application/json', 
                            data=json.dumps(self.user))
        response = self.app.post('/api/v2/auth/login', 
                            content_type='application/json', 
                            data=json.dumps({"user_email": "sonifdggak1234@gmail.com", 
                            "user_password": "fdfghh"}))
        self.assertEqual(response.status_code, 401)

    def test_login_wrong_password(self):
        """Ensures that a user can't log on with wrong password"""
        response = self.app.post('/api/v2/auth/register', 
                            content_type='application/json', 
                            data=json.dumps(self.user))
        response = self.app.post('/api/v2/auth/login', 
                            content_type='application/json', 
                            data=json.dumps({"user_email": "soniak@gmail.com", 
                            "user_password": "67kK0"}))
        self.assertEqual(response.status_code, 401)

    def test_login_missing_password(self):
        """Ensures that a user can't log on with missing password"""
        response = self.app.post('/api/v2/auth/register', 
                            content_type='application/json', 
                            data=json.dumps(self.user))
        response = self.app.post('/api/v2/auth/login', 
                            content_type='application/json', 
                            data=json.dumps({"user_email": "soniak@gmail.com"}))
        self.assertEqual(response.status_code, 400)

    def test_login_missing_email(self):
        """Ensures that a user can't log on with missing password"""
        response = self.app.post('/api/v2/auth/register', 
                            content_type='application/json', 
                            data=json.dumps(self.user))
        response = self.app.post('/api/v2/auth/login', 
                            content_type='application/json', 
                            data=json.dumps({"user_password": "fjkJKNKE3"}))
        self.assertEqual(response.status_code, 400)

    def test_using_blacklist_token(self):
        """Ensures that a user can't log on with a blacklisted token"""
        register = self.app.post('/api/v2/auth/register', 
                            content_type='application/json', 
                            data=json.dumps(self.user))
        login = self.app.post('/api/v2/auth/login', 
                            content_type='application/json', 
                            data=json.dumps(self.user))
        login_data = json.loads(login.data.decode())
        access_token = login_data["token"]
        logout = self.app.post('/api/v2/auth/logout', 
                            headers={'Authorization': 'Bearer ' + access_token}, 
                            content_type='application/json')
        logout = self.app.post('/api/v2/auth/logout', 
                            headers={'Authorization': 'Bearer ' + access_token}, 
                            content_type='application/json')
        self.assertEqual(logout.status_code, 403)

    def tests_user_logout(self):
        """ test a user logs out successfully """
        register = self.app.post('/api/v2/auth/register', 
                            content_type='application/json', 
                            data=json.dumps(self.user))
        login = self.app.post('/api/v2/auth/login', 
                            content_type='application/json', 
                            data=json.dumps(self.user))
        login_data = json.loads(login.data.decode())
        access_token = login_data["token"]
        logout = self.app.post('/api/v2/auth/logout', 
                            headers={'Authorization': 'Bearer ' + access_token}, 
                            content_type='application/json')
        self.assertEqual(logout.status_code, 200)

    def test_user_reset_password(self):
        """ tests a registered user can reset their password """
        response = self.app.post('/api/v2/auth/register', 
                            content_type = 'application/json', 
                            data = json.dumps(self.user))
        response = self.app.post('/api/v2/auth/reset-password', 
                            content_type = 'application/json',
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            data = json.dumps({'user_email': 'soniak@gmail.com', 
                            'user_password': 'qouyWerty123'}))
        self.assertEqual(response.status_code, 200)

    def test_user_reset_password_invalid_token(self):
        """ tests a registered user can reset their password """
        response = self.app.post('/api/v2/auth/register', 
                            content_type = 'application/json', 
                            data = json.dumps(self.user))
        response = self.app.post('/api/v2/auth/reset-password', 
                            content_type = 'application/json',
                            headers={'Authorization': 'Bearer ' + \
                            'hdshdgfgfdfdf.fkjdfhjfdhjfdjd.sdjdjdjdj'}, 
                            data = json.dumps({'user_email': 'soniak@gmail.com', 
                            'user_password': 'qouyWerty123'}))
        self.assertEqual(response.status_code, 401)

    def test_another_user_reset_password(self):
        """ tests a registered user can reset another user's password """
        register_one = self.app.post('/api/v2/auth/register', 
                            content_type = 'application/json', 
                            data = json.dumps(self.user))
        register_two = self.app.post('/api/v2/auth/register', 
                            content_type = 'application/json', 
                            data = json.dumps(self.user_two))
        response = self.app.post('/api/v2/auth/reset-password', 
                            content_type = 'application/json',
                            headers={'Authorization': 'Bearer ' + self.get_token_two()}, 
                            data = json.dumps({'user_email': 'soniak@gmail.com', 
                            'user_password': 'qouyWerty123'}))
        self.assertEqual(response.status_code, 401)

    def test_user_reset_password_with_spaces(self):
        """ tests a registered user can reset their password with spaces in the password """
        response = self.app.post('/api/v2/auth/register', 
                            content_type = 'application/json', 
                            data = json.dumps(self.user))
        response = self.app.post('/api/v2/auth/reset-password', 
                            content_type = 'application/json',
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            data = json.dumps({'user_email': 'soniak@gmail.com', 
                            'user_password': 'qouy Werty123'}))
        self.assertEqual(response.status_code, 403)

    def test_user_reset_password_missing_new_password(self):
        """ tests a registered user can reset their password without providing a new password"""
        response = self.app.post('/api/v2/auth/register', 
                            content_type = 'application/json', 
                            data = json.dumps(self.user))
        response = self.app.post('/api/v2/auth/reset-password', 
                            content_type = 'application/json',
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            data = json.dumps({'user_email': 'soniak@gmail.com'}))
        self.assertEqual(response.status_code, 400)

    def test_user_reset_password_missing_email(self):
        """ tests a registered user can reset their password without providing the email"""
        response = self.app.post('/api/v2/auth/register', 
                            content_type = 'application/json', 
                            data = json.dumps(self.user))
        response = self.app.post('/api/v2/auth/reset-password', 
                            content_type = 'application/json',
                    headers={'Authorization': 'Bearer ' + self.get_token()}, 
                    data = json.dumps({'user_email': '', 
                    'user_password': 'qouy Werty123'}))
        self.assertEqual(response.status_code, 403)

    def test_user_reset_password_fail(self):
        """ tests a non-registered user cannot reset their password """
        response = self.app.post('/api/v2/auth/register', 
                            content_type = 'application/json',
                            data = json.dumps(self.user))
        response = self.app.post('/api/v2/auth/reset-password', 
                            content_type = 'application/json',
                            headers={'Authorization': 'Bearer ' + self.get_token()},
                            data = json.dumps({'user_email': 'karungi@gmail.com', 
                            'user_password': 'qWerty123'}))
        self.assertEqual(response.status_code, 404)
        
if __name__ == "__main__":
    unittest.main()
