from werkzeug.security import check_password_hash, generate_password_hash
from flask_restful.reqparse import RequestParser
import re

from resources import *
from models.users import User
from models.blacklists import Blacklist


#Validating the arguments
user_validation = RequestParser(bundle_errors=True)
user_validation.add_argument("user_password", type=str,
                            required=True, help="Password is missing")
user_validation.add_argument("user_email", type=str,
                            required=True, help="Email is missing")
user_validation.add_argument("user_name", type=str,
                            required=False, help="Username is missing")

class UserRegister(Resource):
    """Class to handle user registration"""
    @swag_from("../APIdocs/CreateUser.yml")
    def post(self):
        """"User registration with email and password"""
        user_email = user_validation.parse_args().user_email.strip()  
        user_name = user_validation.parse_args().user_name
        user_password = user_validation.parse_args().user_password.strip()        
        if user_email and user_password and user_name:
            if (' ' in user_password):
                message = {'Message':'Make sure the password has no spaces in!'}
                resp = jsonify(message)
                resp.status_code = 403
                return resp
            if len(user_password) < 8:
                message = {'Message':'Make sure the password is longer than 8 characters!'}
                resp = jsonify(message)
                resp.status_code = 403
                return resp
            if len(user_email) > 60:
                message = {'Message':'Make sure the email is not longer than 60 characters!'}
                resp = jsonify(message)
                resp.status_code = 403
                return resp
            is_user = re.match('^[A-Za-z0-9.]+@[A-Za-z0-9]+\.[A-Za-z0-9.]{,60}$',
                                request.json['user_email'])
            user_name = user_name.strip()
            if is_user:
                user = User.query.filter_by(user_email=request.json['user_email'].\
                                        lower()).first() 
                username =  User.query.filter_by(user_name=request.json['user_name'].strip().\
                                        lower()).first()
                if user is None and username is None:
                    new_user = User(user_email=request.json['user_email'].lower(),
                                    user_name = request.json['user_name'].lower(),
                                    user_password=request.json['user_password'])
                    db.session.add(new_user)
                    db.session.commit()
                    message = {'Message': 'User registered!'} 
                    resp = jsonify(message)
                    resp.status_code = 201
                elif username is not None:
                    message = {'Message':'Username already taken, choose another one!'}
                    resp = jsonify(message)
                    resp.status_code = 409
                else:
                    message = {'Message':'Email address has an account registered!'}
                    resp = jsonify(message)
                    resp.status_code = 409
            else:
                message = {'Message':'Enter valid email!'}
                resp = jsonify(message)
                resp.status_code = 403
        elif user_name is None:
            message = {'Message':'Username is missing!'}
            resp = jsonify(message)
            resp.status_code = 403
        else:
            message = {'Message':'Missing Email!'}
            resp = jsonify(message)
            resp.status_code = 403
        return resp             
     
class UserLogin(Resource):
    """Class to handle user login"""

    @staticmethod
    def user_not_found():
        message = {'message': 'User does not Exist!'}
        resp = jsonify(message)
        resp.status_code = 401
        return resp

    @swag_from("../APIdocs/LoginUser.yml")
    def post(self):
        """"User login with email and password"""
        user_email = user_validation.parse_args().user_email
        userpassword = user_validation.parse_args().user_password
        if user_email and userpassword:
            is_user = re.match('^[A-Za-z0-9.]+@[A-Za-z0-9]+\.[A-Za-z0-9.]+$',
                                request.json['user_email'])
            if is_user:
                user = User.query.filter_by(user_email=request.json['user_email']).first()  
                if user is None:
                    resp = UserLogin.user_not_found()
                    return resp
                else:
                    if check_password_hash(user.user_password, request.json['user_password']):
                        token = jwt.encode({'user' : user.id,
                                            'username' : user.user_name, 
                                            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=130)}, 
                                            app.config['SECRET_KEY'])
                        message = {'message': 'Logged in', 'token' : token.decode('UTF-8')}
                        resp = jsonify(message)
                        resp.status_code = 200
                        return resp
                message = {'message': 'could not log in, wrong password'}
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
        message = {'message': 'Logged out'}
        resp = jsonify(message)
        resp.status_code = 200
        return resp

class UserResetPassword(Resource):
    """Class for resetting user password when the user has forgotten their password"""
    
    @token_required
    @swag_from("../APIdocs/PasswordReset.yml")
    def post(self):
        """Method to help a user reset their password"""
      
        userid = request.data['user']
        user_email = user_validation.parse_args().user_email
        user_password = user_validation.parse_args().user_password

        if user_email and user_password:
            is_user = re.match('^[A-Za-z0-9.]+@[A-Za-z0-9]+\.[A-Za-z0-9.]+$',
                                request.json['user_email'])
            if is_user:
                user = User.query.filter_by(user_email=request.json['user_email']).first()
                if user is not None: 
                    if user.id != userid:
                        message = {'message':"You cannot reset a password for another user!!"}
                        resp = jsonify(message)
                        resp.status_code = 401
                        return resp

                    new_password = request.json['user_password']

                    if (' ' in new_password) == False:
                        user.user_password = generate_password_hash(new_password, method='sha256')
                        db.session.commit()
                        message = {'message': 'Password Reset'}
                        resp = jsonify(message)
                        resp.status_code = 200
                    else:
                        message = {'message':'Invalid Password,\
                                    make sure the password has no spaces in it!'}
                        resp = jsonify(message)
                        resp.status_code = 403
                    return resp 
                else:
                    message = {'message': 'User doesnot exist'}
                    resp = jsonify(message)
                    resp.status_code = 404
                    return resp
        else:
            message = {'message':'Missing/invalid Email!'}
            resp = jsonify(message)
            resp.status_code = 403
            return resp 
