import unittest
import os
import json
from run import BusinessList, BusinessOne, UserRegister, UserLogin
from resources import app, db


class TestBusiness(unittest.TestCase):

    def create_app(self):
        """Creates the app for testing"""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234567890@localhost/testdb'
        return app

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        db.session.remove()
        db.drop_all()
        db.create_all()
        self.user = {'user_email' : 'soniak@gmail.com', 'user_password' : 'qWerty123'}
        self.business = {'business_name': 'MTN Kla', 'location' : 'Kampala', 'category' : 'Telecomm', 
                         'business_profile': 'Best Telecomm Company'}
        self.business_edit = {'business_name': 'MTN-Uganda', 'location' : 'Kampala', 'category' : 'Telecommunications', 
                         'business_profile': 'Best Telecomm Company'}

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def get_token(self):
        """ Generate token """
        register = self.app.post('/api/v2/auth/register', content_type='application/json', data=json.dumps(self.user))
        login = self.app.post('/api/v2/auth/login', content_type='application/json', data=json.dumps(self.user))
        login_data = json.loads(login.data.decode())
        self.access_token = login_data["token"]
        return self.access_token

    def test_create_business_without_authentication(self):
        """Tests whether a user can create a business without token"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            data = json.dumps(self.business))
        self.assertEqual(response.status_code, 404)

    def test_create_business(self):
        """Tests whether a user can create a business"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        self.assertEqual(response.status_code, 201)

    def test_create_business_already_exist(self):
        """Tests creating a business that already exists"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        self.assertEqual(response.status_code, 409)

    def test_create_business_missing_values(self):
        """Tests creating a business with missing fields"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps({'businessName': 'Airtel Uganda','Category' : 'Telecomm', 
                                'businessProfile': 'Best Telecomm Company', 'createdBy': 'Sonia'})
                            )
        self.assertEqual(response.status_code, 400)
    
    def test_editing_business(self):
        """Tests editing a business"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.put('/api/v2/businesses/1', 
                                headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business_edit), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_editing_business_not_exist(self):
        """Tests editing a business that is not registered yet"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        update_response = self.app.put('/api/v2/businesses/2', 
                                headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business_edit), content_type = 'application/json'
                                )
        self.assertEqual(update_response.status_code, 404)

    def test_business_owner_only_can_edit_business(self):
        """Tests whether only a user who created a business can edit it"""
        pass

    def test_deleting_business(self):
        """ tests a business can be deleted"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.delete('/api/v2/businesses/1', headers={'Authorization': 'Bearer ' + self.get_token()}, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_deleting_business_not_exist(self):
        """ checks whether a business exists before it can be deleted"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        del_result = self.app.delete('/api/v2/businesses/2', headers={'Authorization': 'Bearer ' + self.get_token()}, content_type = 'application/json')
        self.assertEqual(del_result.status_code, 404)

    def test_business_owner_only_can_delete_business(self):
        """Tests whether only a user who created a business can delete it"""
        pass

    def test_get_all_businesses(self):
        """Test to get all businesses"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses', headers={'Authorization': 'Bearer ' + self.get_token()}, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_one_business(self):
        """Test to get one business"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses/1', headers={'Authorization': 'Bearer ' + self.get_token()}, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_one_business_not_exist(self):
        """Test to get a business that doesn't exist"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses/2', headers={'Authorization': 'Bearer ' + self.get_token()}, content_type = 'application/json')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
