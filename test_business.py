import unittest
import json
import app

BASE_URL = 'http://127.0.0.1:5000/api/v1/businesses'
BAD_BUSINESS_URL = '{}/6'.format(BASE_URL)
GOOD_BUSINESS_URL = '{}/1'.format(BASE_URL)


class TestBusiness(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    def test_get_one(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["businesses"][0]["businessName"], "MTN")
        self.assertEqual(data["businesses"][0]["Location"], "Kampala")
        self.assertEqual(data["businesses"][0]["Category"], "Telecommunications")
        self.assertEqual(data["businesses"][0]["businessProfile"], "Best telecommunication company in Uganda")

    def test_business_not_exist(self):
        response = self.app.get(BAD_BUSINESS_URL)
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        # check for missing values
        business = {"businessName" : "some_name", "Location" : "some_location", "Category" : "some_category", 'businessProfile': "some_profile"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(business),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
    def test_update(self):
        business = {"businessID": "MTN"}
        response = self.app.put(GOOD_BUSINESS_URL,
                                data=json.dumps(business),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data["business"]["businessName"], "MTN")

    def test_update_error(self):
        # cannot edit non-existing business
        business = {"businessName": "MTN"}
        response = self.app.put(BAD_BUSINESS_URL,
                                data=json.dumps(business),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        response = self.app.delete(GOOD_BUSINESS_URL)
        self.assertEqual(response.status_code, 204)
        response = self.app.delete(BAD_BUSINESS_URL)
        self.assertEqual(response.status_code, 404)  
      
    def test_get_all(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['businesses']), 5)

if __name__ == "__main__":
    unittest.main()