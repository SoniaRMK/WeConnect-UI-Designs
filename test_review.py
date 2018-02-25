import unittest
import json
import app

BASE_URL = 'http://127.0.0.1:5000/api/v1/businesses'
BAD_REVIEW_URL = '{}/6/reviews'.format(BASE_URL)
GOOD_REVIEW_URL = '{}/1/reviews'.format(BASE_URL)


class TestReviews(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    def test_get_all(self):
        response = self.app.get(GOOD_REVIEW_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['reviews']), 5)

    def test_review_not_exist(self):
        response = self.app.get(BAD_REVIEW_URL)
        self.assertEqual(response.status_code, 404)

    def test_post(self, bizid):
        # check for missing values
        review = {'reviewMsg' : 'some_review'}
        response = self.app.post(GOOD_REVIEW_URL,
                                 data=json.dumps(review),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()