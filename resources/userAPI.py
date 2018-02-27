from resources.lib import *

users = []



class UserRegister(Resource):
    def post(self):
        user = {
            'userID' : len(users) + 1,
            'userEmail' : request.json['userEmail'],
            'userPassword' : request.json['userPassword']
            }
        users.append(user)
        return jsonify({'Users': users})

class UserLogin(Resource):
    def post(self):
        #auth = request.authorization
        token = ''
        for u in users:
            if u['userEmail'] == request.json['userEmail'] and u['userPassword'] == request.json['userPassword']:
                token = jwt.encode({'user' : u['userEmail'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        # if user['userEmail'] == request.json['userEmail'] and user['userPass'] == request.json['userPassword']:
            # token = jwt.encode({'user' : email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})

        return make_response('Could not verify!', 401)

       # user = [u for u in users if u['userEmail'] == email and u['userPassword'] == psswd]
       # return jsonify({'user' : user[0]})

class UserLogout(Resource):
    @token_required
    def post(self):
        
        return jsonify({'Logged Out!!'})  

class UserResetPassword(Resource):
    @token_required
    def post(self):
        return jsonify({'Logged Out!!'})       