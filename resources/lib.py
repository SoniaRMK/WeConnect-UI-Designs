import jwt
import json
import datetime
from functools import wraps
from flask import Flask, abort, request, jsonify, make_response, abort
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'Oxa34KLncvfjKEjXkf'

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        # import ipdb
        # ipdb.set_trace()
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

            if not token:
                return jsonify({'message' : 'Token is missing!'})

            try: 
                data = jwt.decode(token, app.config['SECRET_KEY'])
                user = data['user']
                if user:
                    request.data = json.loads(request.data) if len(request.data) else {}
                    request.data['user'] = user
            except:
                return jsonify({'message' : 'Token is invalid!'})

        return func(*args, **kwargs)

    return decorated