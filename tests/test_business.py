import unittest
import os
import json
from run import BusinessList, BusinessOne
from resources import app, db
from models.models import User, Business


class TestBusiness(unittest.TestCase):
    """Class to test business API"""

    def setUp(self):
        self.app=app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234567890@localhost/testdb'
        db.session.close()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_create_business_no_auth(self):
        """Tests to ensure that a user not logged in can't create a business"""
        response = self.app.post('/api/v2/businesses',
                            content_type='application/json',
                            data=json.dumps({"business_name" : "InfoTech Electronics Ltd.", 
                                "business_profile" : "Deals in Mobile phone and Laptop accessories", 
                                "location" : "Kampala", "category" : "Telecommunications", "user_id" : 1})
                            )
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Token is missing!!', response.data)



if __name__ == "__main__":
    unittest.main()