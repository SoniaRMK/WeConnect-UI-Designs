import sys
sys.path.append('..')
from resources import *
import smtplib
import random
from flask_restful.reqparse import RequestParser

users = []
token = ''
#Validating the arguments
user_validation = RequestParser(bundle_errors=True)
user_validation.add_argument("userEmail", type=str, required=True, help="Email must be a valid email")
user_validation.add_argument("userPassword", type=str, required=True, help="Password must be a valid string")


class UserRegister(Resource):
    @swag_from("../APIdocs/CreateUser.yml")
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
            resp.status_code = 201
      
        else:
            message = {
            'status': "Failed",
            'message': 'Email Already registered!',
            }
            resp = jsonify(message)
            resp.status_code = 409

        return resp 
        
class UserLogin(Resource):
    @swag_from("../APIdocs/LoginUser.yml")
    def post(self):
        user_args = user_validation.parse_args()
        for u in users:
            if u['userEmail'] == user_args.userEmail and u['userPassword'] == user_args.userPassword:
                token = jwt.encode({'user' : u['userEmail'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            else:
                message = {
                'status': "Bad Request",
                'message': 'User cannot be verified!',
                }
                resp = jsonify(message)
                resp.status_code = 401
                return resp
        message = {
            'status': "Success",
            'message': 'Logged in',
            'token' : token.decode('UTF-8'),
            }
        resp = jsonify(message)
        resp.status_code = 200
        return resp

class UserLogout(Resource):
    @swag_from("../APIdocs/LogoutUser.yml")
    def post(self):
        return make_response('Successfully Logged out!', 200)

class UserResetPassword(Resource):
    @swag_from("../APIdocs/PasswordReset.yml")
    def post(self):
        resp = jsonify({})
        user_args = user_validation.parse_args()
        for u in users:
            if u['userEmail'] == user_args.userEmail:
                u['userPassword'] = user_args.userPassword
                message = {
                    'status': "Success",
                    'message': 'Password Reset'
                 }
                resp = jsonify(message)
                resp.status_code = 200
            else:
                message = {
                    'status': "Not Found",
                    'message': 'User doesnot exist',
                    }
                resp = jsonify(message)
                resp.status_code = 404
        return resp
