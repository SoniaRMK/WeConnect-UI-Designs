from resources import *
from werkzeug.security import check_password_hash, generate_password_hash
from flask_restful.reqparse import RequestParser
import re
from models.models import User, Blacklist


#Validating the arguments
user_validation = RequestParser(bundle_errors=True)
user_validation.add_argument("user_password", type=str, required=True, help="Password must be a valid string")
#user_validation.add_argument("confirm_password", type=str, required=True, help="Password must be entered twice!")


class UserRegister(Resource):
    """Class to handle user registration"""
    @swag_from("../APIdocs/CreateUser.yml")
    def post(self):
        """"User registration with email and password"""

        user_email = re.match('^[A-Za-z0-9.]+@[A-Za-z0-9]+\.[A-Za-z0-9.]{,100}$', request.json['user_email'])
        user_password=user_validation.parse_args().user_password

        if user_email and user_password:
            user = User.query.filter_by(user_email=request.json['user_email']).first()  
            if user is None:
                new_user = User(user_email=request.json['user_email'],user_password=request.json['user_password'])
                db.session.add(new_user)
                db.session.commit()
                message = {'status': "Success", 'message': 'User registered!',} 
                resp = jsonify(message)
                resp.status_code = 201
                return resp 

            message = {'Message':'User already exists!', 'status': "Conflict"}
            resp = jsonify(message)
            resp.status_code = 409
            return resp 
        else:
            message = {'Message':'Missing/invalid Email or missing Password!', 'status': "Failed"}
            resp = jsonify(message)
            resp.status_code = 403
            return resp       
     
class UserLogin(Resource):
    """Class to handle user login"""
    @swag_from("../APIdocs/LoginUser.yml")
    def post(self):
        """"User login with email and password"""
        user_email = re.match('^[A-Za-z0-9.]+@[A-Za-z0-9]+\.[A-Za-z0-9.]{,100}$', request.json['user_email'])
        userpassword = user_validation.parse_args().user_password
        if user_email and userpassword:
            user = User.query.filter_by(user_email = request.json['user_email']).first()
            if user is None:
                message = {'status': "Bad Request", 'message': 'User does not Exist!'}
                resp = jsonify(message)
                resp.status_code = 401
                return resp
            else:
                if check_password_hash(user.user_password, request.json['user_password']):
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
    @token_required
    def post(self):
        """Method to help a user reset their password"""

        user_email = re.match('^[A-Za-z0-9.]+@[A-Za-z0-9]+\.[A-Za-z0-9.]+$', request.json['user_email'])
        user_password = user_validation.parse_args().user_password

        if user_email and user_password:
            user = User.query.filter_by(user_email=request.json['user_email']).first()
            if user is not None:  
                user.user_password = generate_password_hash(request.json['user_password'], method='sha256')
                db.session.commit()
                message = {
                    'status': "Success",
                    'message': 'Password Reset',
                    }
                resp = jsonify(message)
                resp.status_code = 200           
                return resp

            message = {'status': "Not Found", 'message': 'User doesnot exist'}
            resp = jsonify(message)
            resp.status_code = 404
            return resp
