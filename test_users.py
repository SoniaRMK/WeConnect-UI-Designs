import unittest
import json

import app

BASE_URL = 'http://127.0.0.1:5000/api/v1/auth/register'


class TestUserRegister(unittest.TestCase):

    def test_post(self):

        # valid: both required fields
        user = {"userEmail": "hjk@yyy.com", "userPassword": "jh123"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(user),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['user']['userEmail'], "hjk@yyy.com")
        self.assertEqual(data['user']['userPassword'], 'jh123')


if __name__ == "__main__":
    unittest.main()