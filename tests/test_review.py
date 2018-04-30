
import sys
sys.path.append('..')
import unittest
import json
from resources import app, api
from run import Review, BusinessList
from resources.review_api import reviews
from resources.business_api import businesses, BusinessList


class TestReviews(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.business = {'businessName': 'MTN', 'Location' : 'Kampala', 'Category' : 'Telecomm', 
                        'businessProfile': 'Best Telecomm Company'}
        self.review = {"reviewMsg": "Telecommunications"}

    def tearDown(self):
        reviews.clear()
    
    def test_get_all_reviews_success(self):
        """Tests getting all reviews for a registered business"""
        response = self.app.post('/api/v1/businesses', content_type = 'application/json', 
                            data = json.dumps(self.business))
        response = self.app.post('/api/v1/businesses/1/reviews', content_type = 'application/json', 
                            data = json.dumps(self.review))
        response = self.app.get('/api/v1/businesses/1/reviews', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_all_reviews_not_exist(self):
        """Checks whether a business has reviews before retrieval"""
        response = self.app.post('/api/v1/businesses', content_type = 'application/json', 
                            data = json.dumps(self.business))
        response = self.app.get('/api/v1/businesses/1/reviews', content_type = 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_all_reviews_busines_not_exist(self):
        """Checks whether a business exists before retrieving reviews"""
        response = self.app.get('/api/v1/businesses/1/reviews', content_type = 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_add_review_success(self):
        """Tests adding a review to a registered business"""
        response = self.app.post('/api/v1/businesses', content_type = 'application/json', 
                            data = json.dumps(self.business))
        response = self.app.post('/api/v1/businesses/1/reviews', content_type = 'application/json', 
                            data = json.dumps(self.review))
        self.assertEqual(response.status_code, 200)

    def test_add_review_fail(self):
        """Tests adding a review to a business not yet registered"""
        response = self.app.post('/api/v1/businesses/1/reviews', content_type = 'application/json', 
                            data = json.dumps(self.review))
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
