import unittest
import json
import app

BASE_URL = '/api/v2/businesses'
BAD_REVIEW_URL = '{}/6/reviews'.format(BASE_URL)
GOOD_REVIEW_URL = '{}/1/reviews'.format(BASE_URL)


class TestReviews(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True
        reviews = [
                {
                    "reviewMsg": "Telecommunications",
                    "businessID": 1,
                    "createdBy": "Sonia"
            }
        ]

    def test_get_all(self):
        response = self.app.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(len(data['reviews']), 5)

    def test_review_not_exist(self):
        response = self.app.get(BAD_REVIEW_URL)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        # check for missing values
        review = {'reviewMsg' : 'some_review'}
        response = self.app.post(GOOD_REVIEW_URL,
                                 data=json.dumps(review),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()