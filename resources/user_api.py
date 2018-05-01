from resources import *
import smtplib
import random
from flask_restful.reqparse import RequestParser
from models.models import User, Blacklist


#Validating the arguments
user_validation = RequestParser(bundle_errors=True)
user_validation.add_argument("user_email", type=str, required=True, help="Email must be a valid email")
user_validation.add_argument("user_password", type=str, required=True, help="Password must be a valid string")


class UserRegister(Resource):
    """Class to handle user registration"""
    @swag_from("../APIdocs/CreateUser.yml")
    def post(self):
        """"User registration with email and password"""
        user = User(user_email=user_validation.parse_args().user_email, user_password=user_validation.parse_args().user_password)
        try:
            db.session.add(user)
            db.session.commit()
            message = {'status': "Success", 'message': 'User registered!',} 
            resp = jsonify(message)
            resp.status_code = 201
            return resp 
        except:
            message = {'Message':'User already exists!', 'status': "Conflict"}
            resp = jsonify(message)
            resp.status_code = 409
            return resp 
        else:
            message = {'Message':'Missing Email or Password!', 'status': "Failed"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp       
     
class UserLogin(Resource):
    """Class to handle user login"""
    @swag_from("../APIdocs/LoginUser.yml")
    def post(self):
        """"User login with email and password"""
        useremail = user_validation.parse_args().user_email
        userpassword = user_validation.parse_args().user_password
        user = User.query.filter_by(user_email = useremail).first()
        if not user:
            message = {'status': "Bad Request", 'message': 'User does not Exist!'}
            resp = jsonify(message)
            resp.status_code = 401
            return resp
        if user.user_password == userpassword:
            token = jwt.encode({'user' : user.id, 
                                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 
                               app.config['SECRET_KEY'])
            message = {'status': "Success", 'message': 'Logged in', 'token' : token.decode('UTF-8')}
            resp = jsonify(message)
            resp.status_code = 200
            return resp
        message = {'status': "Failed", 'message': 'could not log in, wrong password'}
        resp = jsonify(message)
        resp.status_code = 401
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
        message = {'status': "Success", 'message': 'Logged out'}
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
        userpassword = request.json['user_password']
        confirmpassword = request.json['confirm_password']
        if userpassword != confirmpassword:
            message = {
            'status': "Failed",
            'message': 'Passwords do not match',
            }
            resp = jsonify(message)
            resp.status_code = 400
            return resp
        else:
            user.user_password = userpassword
        db.session.commit()
        message = {
        'status': "Success",
        'message': 'Password Reset',
        'New Password': user.user_password,
        }
        resp = jsonify(message)
        resp.status_code = 200           
        return resp
