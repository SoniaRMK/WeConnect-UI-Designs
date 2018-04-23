from resources import *
import smtplib
import random
from flask_restful.reqparse import RequestParser
from models.models import User


token = ''

#Validating the arguments
user_validation = RequestParser(bundle_errors=True)
#user_validation.add_argument("displayName", type=str, required=True, help="Name must be a valid string")
user_validation.add_argument("user_email", type=str, required=True, help="Email must be a valid email")
user_validation.add_argument("user_password", type=str, required=True, help="Password must be a valid string")


class UserRegister(Resource):
    @swag_from("../APIdocs/CreateUser.yml")
    def post(self): 
       # user_args = user_validation.parse_args()
        #user_email = user_validation.parse_args().user_email
        #user_password = user_validation.parse_args().user_password
        user = User(user_email=user_validation.parse_args().user_email, user_password=user_validation.parse_args().user_password)

        """ if not user_email or not user_password:
            message = {
                'status': "Bad Request",
                'message': 'User cannot be registered!',
                }
            resp = jsonify(message)
            resp.status_code = 400
            return resp """
        try:
            #user = models.User(user_email, user_password)
            db.session.add(user)
            db.session.commit()
            message = {
                'status': "Success",
                'message': 'User registered!',
                }
            resp = jsonify(message)
            resp.status_code = 201
        except:
            message = {
                'status': "Conflict",
                'message': 'User already exists!',
                }
            resp = jsonify(message)
            resp.status_code = 409 
        
        db.session.close()
        return resp       

        
class UserLogin(Resource):
    @swag_from("../APIdocs/LoginUser.yml")
    def post(self):
        useremail = user_validation.parse_args().user_email
        userpassword = user_validation.parse_args().user_password

        if not useremail or not userpassword:
            message = {
                'status': "Bad Request",
                'message': 'Password and/or Email are missing!',
                }
            resp = jsonify(message)
            resp.status_code = 401
            return resp
        
        user = User.query.filter_by(user_email = useremail).first()
        if not user:
            message = {
                'status': "Bad Request",
                'message': 'User does not Exist!',
                }
            resp = jsonify(message)
            resp.status_code = 401
            return resp
        if user.user_password == userpassword:
            token = jwt.encode({
                            'user' : user.id, 
                            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

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
    @token_required
    def post(self):
        message = {
            'status': "Success",
            'message': 'Logged out',
            }
        resp = jsonify(message)
        resp.status_code = 200
        return resp

class UserResetPassword(Resource):
    @swag_from("../APIdocs/PasswordReset.yml")
    def post(self):
        resp = jsonify({})
        user_args = user_validation.parse_args()
        for user in users:
            if user['userEmail'] == user_args.userEmail:
                user['userPassword'] = user_args.userPassword
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
