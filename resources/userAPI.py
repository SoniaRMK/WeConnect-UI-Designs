from resources.lib import *

users = [
    {'userID' : 1, 'userEmail' : 'aws@xxx.com', 'userPassword' : 'qwer123' },
    {'userID' : 2, 'userEmail' : 'hjk@yyy.com', 'userPassword' : 'jh123' }
]

class UserRegister(Resource):
    def post(self):
        user = {
            'userID' : users[-1]['userID'] + 1,
            'userEmail' : request.json['userEmail'],
            'userPassword' : request.json['userPassword']
            }
        users.append(user)
        return jsonify({'Users': users})

class UserLogin(Resource):
    def post(self, email, psswd):
        user = [u for u in users if u['userEmail'] == email and u['userPassword'] == psswd]
        return jsonify({'user' : user[0]})

class UserLogout(Resource):
    def post(self):
        return jsonify({'Logged Out!!'})        