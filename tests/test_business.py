import unittest
import os
import json
from run import BusinessList, BusinessOne, UserRegister, UserLogin
from resources import app, db


class TestBusiness(unittest.TestCase):

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
        self.user = {'user_email' : 'soniak@gmail.com', 'user_password' : 'qWerty123'}
        self.user_two = {'user_email' : 'kaynuts@gmail.com', 'user_password' : '12345678'}
        self.business = {'business_name': 'MTN Kla', 'location' : 'Kampala', 'category' : 'Telecomm', 
                         'business_profile': 'Best Telecomm Company'}
        self.business_edit = {'business_name': 'MTN-Uganda', 'location' : 'Kampala', 'category' : 'Telecommunications', 
                         'business_profile': 'Best Telecomm Company'}
        self.business_edit_duplicate = {'business_name': 'MTN Kawempe', 'location' : 'Kampala', 'category' : 'Telecomm', 
                         'business_profile': 'Best Telecomm Company'}
        self.business_two = {'business_name': 'MTN Kawempe', 'location' : 'Kampala', 'category' : 'Telecomm', 
                         'business_profile': 'Best Telecomm Company'}

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def get_token(self):
        """ Generate token using details of self.user """
        register = self.app.post('/api/v2/auth/register', content_type='application/json', data=json.dumps(self.user))
        login = self.app.post('/api/v2/auth/login', content_type='application/json', data=json.dumps(self.user))
        login_data = json.loads(login.data.decode())
        self.access_token = login_data["token"]
        return self.access_token

    def get_token_two(self):
        """ Generate token using details of self.user_two"""
        register = self.app.post('/api/v2/auth/register', content_type='application/json', data=json.dumps(self.user_two))
        login = self.app.post('/api/v2/auth/login', content_type='application/json', data=json.dumps(self.user_two))
        login_data = json.loads(login.data.decode())
        self.access_token_two = login_data["token"]
        return self.access_token_two

    def test_create_business_without_authentication(self):
        """Tests whether a user can create a business without token"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', data = json.dumps(self.business))
        self.assertEqual(response.status_code, 404)

    def test_create_business_success(self):
        """Tests whether a user can create a business"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', headers={'Authorization': 'Bearer ' + self.get_token()}, 
                            data = json.dumps({'business_name': 'MTN Uganda', 'location' : 'Kampala', 'category' : 'Telecomm', 
                            'business_profile': 'Best Telecomm Company'}))
        self.assertEqual(response.status_code, 201)
    
    def test_create_business_already_exist(self):
        """Tests creating a business that already exists"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer '  + self.get_token()}, data = json.dumps(self.business))
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer '  + self.get_token()}, data = json.dumps(self.business))
        self.assertEqual(response.status_code, 409)

    def test_create_business_missing_values(self):
        """Tests creating a business with missing fields"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer '  + self.get_token()}, 
                            data = json.dumps({'business_name': 'Airtel Uganda','category' : 'Telecomm', 
                                                'business_profile': 'Best Telecomm Company'}))
        self.assertEqual(response.status_code, 400)
    
    def test_create_business_with_many_spaces_in_business_name(self):
        """Tests creating a business with many spaces in business name"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer '  + self.get_token()}, 
                            data = json.dumps({'business_name': 'Airtel    Uganda','location' : 'Kampala', 'category' : 'Telecomm', 
                                                'business_profile': 'Best Telecomm Company'}))
        self.assertEqual(response.status_code, 403)

    def test_create_business_with_many_spaces_in_business_location(self):
        """Tests creating a business with many spaces in business laocation name"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer '  + self.get_token()}, 
                            data = json.dumps({'business_name': 'Airtel Uganda','location' : 'Kampala   Road', 'category' : 'Telecomm', 
                                                'business_profile': 'Best Telecomm Company'}))
        self.assertEqual(response.status_code, 403)

    def test_create_business_with_many_spaces_in_business_category(self):
        """Tests creating a business with many spaces in business category name"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer '  + self.get_token()}, 
                            data = json.dumps({'business_name': 'Airtel Uganda','location' : 'Kampala Road', 'category' : 'Telecomm  and   Electronics', 
                                                'business_profile': 'Best Telecomm Company'}))
        self.assertEqual(response.status_code, 403)

    def test_create_business_with_long_name(self):
        """Tests creating a business with a business name longer than 60 characters"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer '  + self.get_token()}, 
                            data = json.dumps({'business_name': 'Airtel UgandaAirtel UgandaAirtel UgandaAirtel UgandaAirtel UgandaAirtel UgandaAirtel UgandaAirtel Uganda','location' : 'Kampala', 'category' : 'Telecomm', 
                                                'business_profile': 'Best Telecomm Company'}))
        self.assertEqual(response.status_code, 403)

    def test_create_business_with_long_category_name(self):
        """Tests creating a business with a business category longer than 60 characters"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer '  + self.get_token()}, 
                            data = json.dumps({'business_name': 'Airtel Uganda','location' : 'Kampala', 'category' : 'TelecommunicationsTelecommunicationsTelecommunicationsTelecommunicationsTelecommunicationsTelecommunicationsTelecommunications', 
                                                'business_profile': 'Best Telecomm Company'}))
        self.assertEqual(response.status_code, 403)

    def test_create_business_with_long_location_name(self):
        """Tests creating a business with a business location longer than 60 characters"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer '  + self.get_token()}, 
                            data = json.dumps({'business_name': 'Airtel Uganda','location' : 'KampalaKampalaKampalaKampalaKampalaKampalaKampalaKampalaKampalaKampalaKampala', 'category' : 'Telecommunications', 
                                                'business_profile': 'Best Telecomm Company'}))
        self.assertEqual(response.status_code, 403)

    def test_editing_business_success(self):
        """Tests editing a business"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.put('/api/v2/businesses/1', content_type = 'application/json',
                                headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business_edit)) 
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
        register = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        update_response = self.app.put('/api/v2/businesses/1', headers={'Authorization': 'Bearer ' + self.get_token_two()}, 
                                data = json.dumps(self.business_edit), content_type = 'application/json')
        self.assertEqual(update_response.status_code, 401)

    # def test_business_edit_business_name_already_exist(self):
    #     """Tests to ensure that the new business name doesn't already exist"""
    #     register = self.app.post('/api/v2/businesses', content_type = 'application/json', 
    #                         headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
    #     register_another = self.app.post('/api/v2/businesses', content_type = 'application/json', 
    #                         headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business_two))
    #     update_response = self.app.put('/api/v2/businesses/1', headers={'Authorization': 'Bearer ' + self.get_token()}, 
    #                             data = json.dumps(self.business_two), content_type = 'application/json')
    #     self.assertIn(b'jhswhjsfjh', update_response.data)
    #     self.assertEqual(update_response.status_code, 409)

    def test_edit_business_with_many_spaces_in_business_name(self):
        """Tests editing a business with many spaces in business name"""
        register = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.put('/api/v2/businesses/1', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer '  + self.get_token()}, 
                            data = json.dumps({'business_name': 'Airtel    Uganda','location' : 'Kampala', 'category' : 'Telecomm', 
                                                'business_profile': 'Best Telecomm Company'}))
        self.assertEqual(response.status_code, 403)

    def test_edit_business_with_many_spaces_in_business_location(self):
        """Tests editing a business with many spaces in business laocation name"""
        register = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.put('/api/v2/businesses/1', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer '  + self.get_token()}, 
                            data = json.dumps({'business_name': 'Airtel Uganda','location' : 'Kampala   Road', 'category' : 'Telecomm', 
                                                'business_profile': 'Best Telecomm Company'}))
        self.assertEqual(response.status_code, 403)

    def test_edit_business_with_many_spaces_in_business_category(self):
        """Tests editing a business with many spaces in business category name"""
        register = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.put('/api/v2/businesses/1', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer '  + self.get_token()}, 
                            data = json.dumps({'business_name': 'Airtel Uganda','location' : 'Kampala Road', 'category' : 'Telecomm  and   Electronics', 
                                                'business_profile': 'Best Telecomm Company'}))
        self.assertEqual(response.status_code, 403)

    def test_edit_business_with_long_name(self):
        """Tests editing a business with a business name longer than 60 characters"""
        register = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.put('/api/v2/businesses/1', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer '  + self.get_token()}, 
                            data = json.dumps({'business_name': 'Airtel UgandaAirtel UgandaAirtel UgandaAirtel UgandaAirtel UgandaAirtel UgandaAirtel UgandaAirtel Uganda','location' : 'Kampala', 'category' : 'Telecomm', 
                                                'business_profile': 'Best Telecomm Company'}))
        self.assertEqual(response.status_code, 403)

    def test_edit_business_with_long_category_name(self):
        """Tests editing a business with a business category longer than 60 characters"""
        register = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.put('/api/v2/businesses/1', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer '  + self.get_token()}, 
                            data = json.dumps({'business_name': 'Airtel Uganda','location' : 'Kampala', 'category' : 'TelecommunicationsTelecommunicationsTelecommunicationsTelecommunicationsTelecommunicationsTelecommunicationsTelecommunications', 
                                                'business_profile': 'Best Telecomm Company'}))
        self.assertEqual(response.status_code, 403)

    def test_edit_business_with_long_location_name(self):
        """Tests creating a business with a business location longer than 60 characters"""
        register = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.put('/api/v2/businesses/1', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer '  + self.get_token()}, 
                            data = json.dumps({'business_name': 'Airtel Uganda','location' : 'KampalaKampalaKampalaKampalaKampalaKampalaKampalaKampalaKampalaKampalaKampala', 'category' : 'Telecommunications', 
                                                'business_profile': 'Best Telecomm Company'}))
        self.assertEqual(response.status_code, 403)

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
        register = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        del_response = self.app.delete('/api/v2/businesses/1', headers={'Authorization': 'Bearer ' + self.get_token_two()}, 
                                data = json.dumps(self.business_edit), content_type = 'application/json')
        self.assertEqual(del_response.status_code, 401)

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

    def test_get_all_businesses(self):
        """Test to get all businesses with no parameters provided"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_all_businesses_with_search_term(self):
        """Test to get all businesses with with only search term"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q="MTN"', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_all_businesses_with_limit(self):
        """Test to get all businesses with with only limit"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?limit=1', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_get_all_businesses_with_search_term_and_limit(self):
        """Test to get all businesses with with search term and limit"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q="MTN"&limit="2"', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_all_businesses_with_search_term_and_location(self):
        """Test to get all businesses with with search term and location"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q="MTN"&location="Kampala"', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_all_businesses_with_search_term_and_category(self):
        """Test to get all businesses with with search term and category"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q="MTN"&category="Construction"', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_all_businesses_with_search_term_category_and_location(self):
        """Test to get all businesses with with search term, location and category"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q="MTN"&category="Telecomm"&location="Kampala"', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_all_businesses_with_search_term_location_and_limit(self):
        """Test to get all businesses with with search term, location and limit"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q="MTN"&limit="2"&location="Kampala"', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_all_businesses_with_search_term_category_and_limit(self):
        """Test to get all businesses with with search term, category and limit"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q="MTN"&limit="2"&category="Construction"', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_all_businesses_with_search_term_location_category_and_limit(self):
        """Test to get all businesses with with search term, category, location and limit"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q="MTN"&limit="2"&location="Kampala"&category="Construction"', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_limit_less_than_zero(self):
        """Test to get all businesses with with limit"""
        response = self.app.post('/api/v2/businesses', content_type = 'application/json', 
                            headers={'Authorization': 'Bearer ' + self.get_token()}, data = json.dumps(self.business))
        response = self.app.get('/api/v2/businesses?q=ganda&limit=-1', content_type = 'application/json')
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
