from resources import *
import smtplib
import random
from flask_restful.reqparse import RequestParser
from models.models import User, Blacklist


token = ''

#Validating the arguments
user_validation = RequestParser(bundle_errors=True)
user_validation.add_argument("user_email", type=str, required=True, help="Email must be a valid email")
user_validation.add_argument("user_password", type=str, required=True, help="Password must be a valid string")


class UserRegister(Resource):
    @swag_from("../APIdocs/CreateUser.yml")
    def post(self): 
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
            resp.status_code = 400
            return resp
        
        user = User.query.filter_by(user_email = useremail).first()
        if not user:
            message = {
                'status': "Bad Request",
                'message': 'User does not Exist!',
                }
            resp = jsonify(message)
            resp.status_code = 400
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
    """Class for logging out a user"""

    @swag_from("../APIdocs/LogoutUser.yml")
    @token_required
    def post(self):
        """Logs out a user"""
        
        authorization = request.headers.get("Authorization")
        if authorization:
            token = authorization.split(" ")[1]
        token_blacklist = Blacklist(token)
        db.session.add(token_blacklist)
        db.session.commit()

        message = {
            'status': "Success",
            'message': 'Logged out',
            }
        resp = jsonify(message)
        resp.status_code = 200
        return resp

class UserResetPassword(Resource):
    """Class for resetting user password when the user has forgotten their password"""
    @swag_from("../APIdocs/PasswordReset.yml")
    def post(self):
        """Method to help a user reset their password"""
        user_email = request.json['user_email']
        user = User.query.filter_by(user_email=user_email).first()
        if not user:
            message = {
                'status': "Not Found",
                'message': 'User doesnot exist',
                }
            resp = jsonify(message)
            resp.status_code = 404
            return resp
        user.user_password = "QwhsdE" + str(random.randrange(10000))
        db.session.commit()
        message = {
            'status': "Success",
            'message': 'Password Reset',
            'New Password': user.user_password,
            }
        resp = jsonify(message)
        resp.status_code = 200
        return resp
