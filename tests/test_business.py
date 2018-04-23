import unittest
import os
import json
import jwt
from run import BusinessList, BusinessOne
from resources import app, db
from models.models import User, Business


class TestBusiness(unittest.TestCase):
    """Class to test business API"""

    def setUp(self):
        self.app=app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        db.session.close()
        db.drop_all()
        db.create_all()

        db.session.add(User(user_email='abc123@yyy.zzz', user_password='67890'))
        db.session.add(Business(business_name="MTN Uganda", business_profile="Best Telecommunications Company", location="Kampala", category="Telecommunications", user_id=1))
        db.session.add(Business(business_name="Cafe Javas", business_profile="Exotic meals and fun drinks", location="Mbarara", category="Food and Beverages", user_id=1))
        db.session.commit()
        login = self.app.post('/api/v2/auth/login',
                            content_type='application/json',
                            data=json.dumps({"user_email": "abc@yyy.zzz", "user_password": "67890"})
                            )
        login_data = json.loads(login.data.decode('UTF-8'))
        print(login_data)
        self.token = login_data["token"]

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

    def test_get_all_businesses_fail(self):
        """checks whether there are businesses registered for retrieving"""
        response = self.app.get('/api/v2/businesses',
                            headers={'Authorization': 'Bearer {}'.format(self.token)},
                            )
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'No businesses found!', response.data)

    def test_create_business(self):
        """Tests that a business has been created"""
        business = {"business_name" : "InfoTech Electronics Ltd.",
                    "business_profile" : "Deals in Mobile phone and Laptop accessories",
                    "location" : "Kampala",                                 
                    "category" : "Telecommunications"
                    }
        response = self.app.post('/api/v2/businesses',
                             headers={'Authorization': 'Bearer {}'.format(self.token)},
                            content_type='application/json',
                            data=json.dumps(business)
                            )
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Business registered!', response.data)

    # def test_create_business_already_exists(self):
    #     """Test to avoid duplication of a business on creation"""
    #     response = self.app.post('/api/v2/businesses',
    #                         headers={'Authorization': 'Bearer {}'.format(self.access_token)},

    #                         content_type='application/json',
    #                         data=json.dumps({"business_name" : "MTN Uganda", 
    #                             "business_profile" : "Best Telecommunications Company", 
    #                             "location" : "Kampala", "category" : "Telecommunications", "user_id" : 1})
    #                         )
    #     self.assertEqual(response.status_code, 409)
    #     self.assertIn(b'Business already Exists!', response.data)

    # def test_create_business_missing_credentials(self):
    #     """Ensure that a business is not created with missing credentials"""
    #     response = self.app.post('/api/v2/businesses',
    #                         #headers={'Authorization': 'Bearer {}'.format(self.access_token)},
    #                         content_type='application/json',
    #                         data=json.dumps({"business_name" : "MTN Uganda"})
    #                         )
    #     self.assertEqual(response.status_code, 406)
    #     self.assertIn(b'Missing fields!', response.data)

    # def test_get_all_businesses(self):
    #     """Ensure that all business registred can be retrieved"""
    #     response = self.app.get('/api/v2/businesses',
    #                         #headers={'Authorization': 'Bearer {}'.format(self.access_token)},
    #                         )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b,'Businesses found!', response.data)
        
    # def test_get_one_business(self):
    #     """Ensure that a business is retrieved given its ID"""
    #     response = self.app.get('/api/v2/businesses/1',
    #                         #headers={'Authorization': 'Bearer {}'.format(self.access_token)},
    #                         )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b,'Business Found!', response.data)

    # def test_get_one_business_fail(self):
    #     """checks whether a business exists before retrieval"""
    #     response = self.app.get('/api/v2/businesses/3',
    #                         #headers={'Authorization': 'Bearer {}'.format(self.access_token)},
    #                         )
    #     self.assertEqual(response.status_code, 404)
    #     self.assertIn(b,'Business not Found!', response.data)
        
    # def test_delete_a_business(self):
    #     """Ensure that a business is deleted given its ID"""
    #     response = self.app.delete('/api/v2/businesses/1',
    #                         #headers={'Authorization': 'Bearer {}'.format(self.access_token)},
    #                         )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b,'Business successfully Deleted!', response.data)

    # def test_delete_a_business_fail(self):
    #     """checks whether a business exists before deletion"""
    #     response = self.app.delete('/api/v2/businesses/3',
    #                         #headers={'Authorization': 'Bearer {}'.format(self.access_token)},
    #                         )
    #     self.assertEqual(response.status_code, 404)
    #     self.assertIn(b,'Business not Found!', response.data)


    # def test_update_a_business(self):
    #     """Ensure that a business is edited and updated given its ID"""
    #     response = self.app.put('/api/v2/businesses/1',
    #                         #headers={'Authorization': 'Bearer {}'.format(self.access_token)},
    #                         content_type='application/json',
    #                         data=json.dumps({"business_name" : "MTN Uganda", 
    #                             "business_profile" : "Best Telecommunications Company in Uganda and beyond", 
    #                             "location" : "Kampala", "category" : "Telecommunications", "user_id" : 1})
    #                         )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b,'Business successfully Updated!', response.data)

    # def test_update_a_business_fail(self):
    #     """checks whether a business exists before editing/updating it"""
    #     response = self.app.put('/api/v2/businesses/3',
    #                         #headers={'Authorization': 'Bearer {}'.format(self.access_token)},
    #                         )
    #     self.assertEqual(response.status_code, 404)
    #     self.assertIn(b,'Business not Found!', response.data)

if __name__ == "__main__":
    unittest.main()