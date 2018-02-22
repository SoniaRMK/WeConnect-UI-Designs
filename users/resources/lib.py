from flask import Flask, abort, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)