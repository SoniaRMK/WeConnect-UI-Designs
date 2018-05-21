from resources import app, db
from werkzeug.security import generate_password_hash
from flask import jsonify


class Blacklist(db.Model):
    """Blacklisted Tokens"""
    
    __tablename__ = 'blacklists'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    def __init__(self,token):
        self.token = token
        db.create_all()
