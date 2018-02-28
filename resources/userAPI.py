from resources.lib import *
from flask_restful.reqparse import RequestParser


users = []

#Validating the arguments
user_validation = RequestParser(bundle_errors=True)
user_validation.add_argument("userEmail", type=str, required=True, help="Email must be a valid email")
user_validation.add_argument("userPassword", type=str, required=True, help="Password must be a valid email")


class UserRegister(Resource):
    def post(self): 
        user_args = user_validation.parse_args()     
        user = {
            'userID' : len(users) + 1,
            'userEmail' : user_args.userEmail,            
            'userPassword' : user_args.userPassword
            }
        use = [u for u in users if user_args.userEmail == u['userEmail']]
        if len(use) == 0:
            users.append(user)
            message = {
            'status': "success",
            'message': 'User Successfully Created!!',
            }
            resp = jsonify(message)
            resp.status_code = 200
      
        else:
            message = {
            'status': "Failed",
            'message': 'Email Already registered!',
            }
            resp = jsonify(message)
            resp.status_code = 400

        return resp 
        
class UserLogin(Resource):
    def post(self):
        user_args = user_validation.parse_args()
        token = ''
        for u in users:
            if u['userEmail'] == user_args.userEmail and u['userPassword'] == user_args.userPassword:
                token = jwt.encode({'user' : u['userEmail'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            else:
                return make_response('Could not verify!', 401)
        return jsonify({'token' : token.decode('UTF-8')})

class UserLogout(Resource):
    @token_required
    def post(self):
        
        return jsonify({'Logged Out!!'})  

class UserResetPassword(Resource):
    def post(self):
        # for u in users:
        #     if u['userEmail'] == request.json['userEmail']: 
        #         u['userPassword'] == request.json['userPassword']  
        #         users.append(u)  
        return jsonify({'Password has been reset!!'})       