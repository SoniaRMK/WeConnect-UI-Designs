from flask import Flask, abort, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

users = [
    {'userID' : 1, 'userEmail' : 'aws@xxx.com', 'userPassword' : 'qwer123' },
    {'userID' : 2, 'userEmail' : 'hjk@yyy.com', 'userPassword' : 'jh123' }
]

class User(Resource):
    def post(self):
        user = {
            'userID' : users[-1]['userID'] + 1,
            'userEmail' : request.json['userEmail'],
            'userPassword' : request.json['userPassword']
            }
        users.append(user)
        return jsonify({'Users': users})

class Login(Resource):
    def post(self, email, password):
        #if email == ('userEmail') and password ==('userPassword'):
            message = 'Login Successful!'
        else:
            message = 'Invalid Credentials.'
        response = jsonify({'message':message})
        return response

api.add_resource(User, '/api/auth/register')
api.add_resource(Login, '/api/auth/login')

if __name__ == '__main__':
    app.run(debug=True)