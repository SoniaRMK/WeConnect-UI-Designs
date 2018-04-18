import jwt
import json
import datetime
from functools import wraps
from flask import Flask, abort, request, jsonify, make_response, abort
from flask_restful import Resource, Api
from flasgger import Swagger, swag_from


app = Flask(__name__)
app.config["SWAGGER"] = {
            'swagger': '2.0',
            'title': 'WeConnect API',
            'description': "WeConnect provides a platform that brings businesses and individuals together.This platform creates awareness for businesses and gives the users the ability to write reviews about the businesses they have interacted with.",
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
app.config['SECRET_KEY'] = 'Oxa34KLncvfjKEjXkf'
swagger = Swagger(app)
api = Api(app)

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):            
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
            try: 
                data = jwt.decode(token, app.config['SECRET_KEY'])
                user = data['user']
                if user:
                    request.data = json.loads(request.data) if len(request.data) else {}
                    request.data['user'] = user
            except:
                message = {
                    'status': "Unauthorized access attempted!",
                    'message': 'Token is invalid!!',
                    }
                resp = jsonify(message)
                resp.status_code = 401
                return resp
        
        else:
            message = {
            'status': "Unauthorized access attempted!",
            'message': 'Token is missing!!',
            }
            resp = jsonify(message)
            resp.status_code = 401
            return resp

        return func(*args, **kwargs)

    return decorated