from resources import app, db
from werkzeug.security import generate_password_hash
from flask import jsonify
    

class Review(db.Model):
    """Model to create a review"""

    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review_title = db.Column(db.String(60), nullable=False)
    review_msg = db.Column(db.Text, nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    def __init__(self, review_title, review_msg, business_id, user_id):
        self.review_title = review_title
        self.review_msg = review_msg
        self.business_id = business_id
        self.user_id = user_id
        db.create_all()