import jwt
import json
import datetime
from functools import wraps
from flask import Flask, abort, request, jsonify, make_response, abort
from flask_restful import Resource, Api
from flasgger import Swagger, swag_from
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')

# Swagger Config for Documentation
app.config["SWAGGER"] = {
    'swagger': '2.0',
    'title': 'WeConnect API',
    'description': "WeConnect provides a platform that brings businesses and individuals together.\
                    This platform creates awareness for businesses and gives the users the ability\
                    to write reviews about the businesses they have interacted with.",
    'basePath': '',
    'version': '1.0.0',
    'contact': {
                'Developer': 'Sonia RM Karungi',
                'email': 'soniakxxx@gmail.com'
    },
    'license': {
    },
    'tags': [
        {
            'name': 'User',
                    'description': 'The user of the api'
        },
        {
            'name': 'Business',
                    'description': 'Business a user adds,updates, deletes'
        },
        {
            'name': 'Review',
                    'description': 'A review of a business'
        },
    ]
}

# Documentation with Flasgger
swagger = Swagger(app)

db = SQLAlchemy(app)
db.init_app(app)
manager = Manager(app)
migrate = Migrate(app, db)


api = Api(app)


def token_required(func):
    """Function to check for Token required"""
    @wraps(func)
    def decorated(*args, **kwargs):
        from models.blacklists import Blacklist
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
            black_list_token = Blacklist.query.filter_by(token=token).first()
            if black_list_token:
                message = {'message': 'Expired token, Login again!!'}
                resp = jsonify(message)
                resp.status_code = 403
                return resp
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                user = data['user']
                if user:
                    request.data = json.loads(request.data) if len(request.data) else {}
                    request.data['user'] = user
            except jwt.InvalidTokenError:
                message = { 'message': 'Token is invalid!!'}
                resp = jsonify(message)
                resp.status_code = 401
                return resp
        else:
            message = {'message': 'Token is missing, Please Login!!'}
            resp = jsonify(message)
            resp.status_code = 404
            return resp
        return func(*args, **kwargs)
    return decorated
