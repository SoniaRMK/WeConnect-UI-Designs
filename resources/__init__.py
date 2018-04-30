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
