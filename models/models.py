from resources import app, SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy(app)
db.init_app(app)

class User(db.Model):
    """Model to create a user"""
    
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(60), nullable=False, unique=True)
    user_password = db.Column(db.String(300), nullable=False,)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())
    #user_name = db.Column(db.String(60))
    businesses = db.relationship('Business', backref='user',
                                 lazy='dynamic')
    def __init__(self, user_email, user_password):
        self.user_email = user_email
        self.user_password = generate_password_hash(user_password, method='sha256')
        db.create_all()
    
class Business(db.Model):
    """Model to create a business"""

    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_name = db.Column(db.String(60), nullable=False, unique=True)
    business_profile = db.Column(db.String(1000), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())
    reviews = db.relationship('Review', backref='business', lazy='dynamic')
    def __init__(self, business_name, business_profile, location, category, user_id):
        self.business_name = business_name#pragma:no cover
        self.business_profile = business_profile#pragma:no cover
        self.location = location#pragma:no cover
        self.category = category#pragma:no cover
        self.user_id = user_id#pragma:no cover
        db.create_all()#pragma:no cover

class Review(db.Model):
    """Model to create a review"""

    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review_msg = db.Column(db.String(1000), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    def __init__(self, review_msg, business_id, user_id):
        self.review_msg = review_msg#pragma:no cover
        self.business_id = business_id#pragma:no cover
        self.user_id = user_id#pragma:no cover
        db.create_all()#pragma:no cover

class Blacklist(db.Model):
    """Blacklisted Tokens"""
    
    __tablename__ = 'blacklists'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    def __init__(self,token):
        self.token = token
        db.create_all()
