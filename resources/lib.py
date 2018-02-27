import jwt
import datetime
from functools import wraps
from flask import Flask, abort, request, jsonify, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'Oxa34KLncvfjKEjXkf'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated