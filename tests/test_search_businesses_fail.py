import unittest
import os
import json
from run import BusinessList, BusinessOne, UserRegister, UserLogin
from resources import app, db


class TestBusiness(unittest.TestCase):
    """Tests the business search and filtering functionality for businesses not found"""

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
        self.user = {'user_email' : 'soniak@gmail.com', 'user_name': 'Kaynuts000', 
                    'user_password' : 'qWerty123'}
        self.user_two = {'user_email' : 'kaynuts@gmail.com', 'user_name': 'Kaynyts000', 
                        'user_password' : '12345678'}
        self.business = {'business_name': 'MTN Kla', 'location' : 'Kampala', 'category' : 'Telecomm', 
                         'business_profile': 'Best Telecomm Company'}
        self.business_edit = {'business_name': 'MTN-Uganda', 'location' : 'Kampala',
                              'category' : 'Telecommunications', 'business_profile': 'Best Telecomm Company'}
        self.business_edit_duplicate = {'business_name': 'MTN Kawempe', 
                                        'location' : 'Kampala', 'category' : 'Telecomm', 
                                        'business_profile': 'Best Telecomm Company'}
        self.business_two = {'business_name': 'MTN Kawempe', 'location' : 'Kampala', 
                             'category' : 'Telecomm', 'business_profile': 'Best Telecomm Company'}

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def get_token(self):
        """ Generate token using details of self.user """
        register = self.app.post('/api/v2/auth/register', 
                                content_type='application/json', data=json.dumps(self.user))
        login = self.app.post('/api/v2/auth/login', 
                                content_type='application/json', data=json.dumps(self.user))
        login_data = json.loads(login.data.decode())
        self.access_token = login_data["token"]
        return self.access_token

    def get_token_two(self):
        """ Generate token using details of self.user_two"""
        register = self.app.post('/api/v2/auth/register', 
                                content_type='application/json', data=json.dumps(self.user_two))
        login = self.app.post('/api/v2/auth/login',
                                content_type='application/json', data=json.dumps(self.user_two))
        login_data = json.loads(login.data.decode())
        self.access_token_two = login_data["token"]
        return self.access_token_two

    def test_get_all_businesses(self):
        """Test to get all businesses with no parameters provided"""
        response = self.app.get('/api/v2/businesses', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            content_type = 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_all_businesses_with_search_term(self):
        """Test to get all businesses with with only search term"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q=airtel', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            content_type = 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_all_businesses_with_limit(self):
        """Test to get all businesses with with only limit"""
        response = self.app.get('/api/v2/businesses?limit=1', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            content_type = 'application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_get_all_businesses_with_search_term_and_limit(self):
        """Test to get all businesses with with search term and limit"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q=airtel&limit=2', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            content_type = 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_all_businesses_with_search_term_and_location(self):
        """Test to get all businesses with with search term and location"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q=airtel&location=Kampala', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            content_type = 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_all_businesses_with_search_term_and_category(self):
        """Test to get all businesses with with search term and category"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q=airtel&category=Telecomm', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            content_type = 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_all_businesses_with_search_term_category_and_location(self):
        """Test to get all businesses with with search term, location and category"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q=airtel&\
                            category=Telecomm&location=Kampala', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            content_type = 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_all_businesses_with_search_term_location_and_limit(self):
        """Test to get all businesses with with search term, location and limit"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q=airtel&limit=2&location=Kampala', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            content_type = 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_all_businesses_with_search_term_category_and_limit(self):
        """Test to get all businesses with with search term, category and limit"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q=airtel&limit=2&category=Telecomm', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            content_type = 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_all_businesses_with_search_term_location_category_and_limit(self):
        """Test to get all businesses with with search term, category, location and limit"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q=airtel&\
                            limit=2&location=Kampala&category=Telecomm', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            content_type = 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_all_businesses_with_search_term_location_category_and_limit_not_found(self):
        """Test to get all businesses with with search term, category, location and limit (no businesses found)"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q=airtel&limit=2&\
                            location=Kampala&category=Telecomm', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            content_type = 'application/json')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
