import sys
sys.path.append('..')
import unittest
import json
from resources import app, api
from run import BusinessList, Business
from resources.business_api import businesses

class TestBusiness(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.business = {'businessName': 'MTN', 'Location' : 'Kampala', 'Category' : 'Telecomm', 
                        'businessProfile': 'Best Telecomm Company'}
        self.business_edit = {'businessName': 'MTN-Uganda', 'Location' : 'Kampala', 'Category' : 'Telecomm', 
                        'businessProfile': 'Best Telecommunications Company'}

    def tearDown(self):
        businesses.clear()

    def test_create_business(self):
        response = self.app.post('/api/v1/businesses', content_type = 'application/json', 
                            data = json.dumps(self.business))
        self.assertEqual(response.status_code, 201)

    def test_create_business_already_exist(self):
        response = self.app.post('/api/v1/businesses', content_type = 'application/json', 
                            data = json.dumps(self.business))
        response = self.app.post('/api/v1/businesses', content_type = 'application/json', 
                            data = json.dumps(self.business))
        self.assertEqual(response.status_code, 400)

    def test_create_business_missing_values(self):
        response = self.app.post('/api/v1/businesses', content_type = 'application/json', 
                            data = json.dumps({'businessName': 'Airtel Uganda','Category' : 'Telecomm', 
                                'businessProfile': 'Best Telecomm Company', 'createdBy': 'Sonia'})
                            )
        self.assertEqual(response.status_code, 400)
    
    def test_editing_business(self):
        response = self.app.post('/api/v1/businesses', content_type = 'application/json', 
                            data = json.dumps(self.business))
        response = self.app.put('/api/v1/businesses/1', 
                                data = json.dumps(self.business_edit), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_editing_business_not_exist(self):
        update_response = self.app.put('/api/v1/businesses/1', 
                                data = json.dumps(self.business_edit), content_type = 'application/json'
                                )
        self.assertEqual(update_response.status_code, 404)

    def test_deleting_business(self):
        """ tests a business can be deleted"""
        response = self.app.post('/api/v1/businesses', content_type = 'application/json', 
                            data = json.dumps(self.business))
        response = self.app.delete('/api/v1/businesses/1', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_deleting_business_not_exist(self):
        """ checks whether a business exists before it can be deleted"""
        del_result = self.app.delete('/api/v1/businesses/1', content_type = 'application/json')
        self.assertEqual(del_result.status_code, 404)

    def test_get_all_businesses(self):
        """Test to get all businesses"""
        response = self.app.post('/api/v1/businesses', content_type = 'application/json', 
                            data = json.dumps(self.business))
        response = self.app.get('/api/v1/businesses', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_one_business(self):
        """Test to get one businesses"""
        response = self.app.post('/api/v1/businesses', content_type = 'application/json', 
                            data = json.dumps(self.business))
        response = self.app.get('/api/v1/businesses/1', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_one_business_not_exist(self):
        """Test to get one businesses"""
        response = self.app.get('/api/v1/businesses/1', content_type = 'application/json')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()