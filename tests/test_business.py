import unittest
import json
# import app
from resources import app

BASE_URL = '/api/v2/businesses'
BAD_BUSINESS_URL = '{}/6'.format(BASE_URL)
GOOD_BUSINESS_URL = '{}/1'.format(BASE_URL)


class TestBusiness(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.businesses = [
            {
                "Category": "Telecommunications",
                "Location": "Kawempe",
                "businessID": 1,
                "businessName": "MTN",
                "businessProfile": "jdshkfasjfhaskdjaskdj",
                "createdBy": "soniakxxx@gmail.com"
            }
        ]

    def test_get_one(self):
        response = self.app.get(GOOD_BUSINESS_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["businesses"][0]["businessName"], "MTN")
        self.assertEqual(data["businesses"][0]["Location"], "Kawempe")
        self.assertEqual(data["businesses"][0]["Category"], "Telecommunications")
        self.assertEqual(data["businesses"][0]["businessProfile"], "jdshkfasjfhaskdjaskdj")

    def test_business_not_exist(self):
        response = self.app.get(BAD_BUSINESS_URL)
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        # check for missing values
        business = {"businessName" : "some_name", "Location" : "some_location", "Category" : "some_category", 'businessProfile': "some_profile"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(business),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 404)
        
    def test_update(self):
        business = {"businessName": "Airtel"}
        response = self.app.put(GOOD_BUSINESS_URL,
                                data=json.dumps(business),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data["business"]["businessName"], "Airtel")

    def test_update_error(self):
        # cannot edit non-existing business
        business = {"businessName": "Smile"}
        response = self.app.put(BAD_BUSINESS_URL,
                                data=json.dumps(business),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        response = self.app.delete(GOOD_BUSINESS_URL)
        self.assertEqual(response.status_code, 404)
        response = self.app.delete(BAD_BUSINESS_URL)
        self.assertEqual(response.status_code, 404)  
      
    def test_get_all(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['businesses']), 1)

if __name__ == "__main__":
    unittest.main()