import unittest
import json

import app

BASE_URL = '/api/v2/auth/register'


class TestUserRegister(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    def test_post(self):

        # valid: both required fields
        user = {"userEmail": "hjk@yyy.com", "userPassword": "jh123"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(user),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()