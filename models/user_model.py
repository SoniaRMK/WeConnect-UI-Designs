from resources import app, db
from werkzeug.security import generate_password_hash
from flask import jsonify


class User(db.Model):
    """Model to create a user"""
    
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(60), nullable=False, unique=True)
    user_password = db.Column(db.String(80), nullable=False,)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())
    businesses = db.relationship('Business', backref='user',
                                 lazy='dynamic')
    def __init__(self, user_email, user_password):
        self.user_email = user_email
        self.user_password = generate_password_hash(user_password, method='sha256')
        db.create_all()