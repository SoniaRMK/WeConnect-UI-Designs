from resources import *
from models.models import Review, Business
from flask_restful.reqparse import RequestParser


"""Validating the arguments"""
review_validation = RequestParser(bundle_errors=True)
review_validation.add_argument("review_msg", type=str, required=True, help="Review Message should be a string")
review_validation.add_argument("review_title", type=str, required=True, help="Review title should be a string")

class ReviewBusiness(Resource):
    """Class for adding and viewing reviews"""
    @swag_from("../APIdocs/ViewReviews.yml")
    @token_required
    def post(self, bizid):
        """Add a review to a business""" 

        user_id = request.data['user']
        business = Business.query.get(bizid)
        if not business:
            message = {'message': "Business you're trying to review is not registered yet!"}
            resp = jsonify(message)
            resp.status_code = 404
            return resp
        if business.user_id == user_id:
            message = {'message': "You cannot review a business you registered!!"}
            resp = jsonify(message)
            resp.status_code = 401
            return resp
        else:
            review = Review(review_title = review_validation.parse_args().review_title, review_msg = review_validation.parse_args().review_msg, business_id = bizid, user_id = user_id)
            db.session.add(review)
            db.session.commit()
            message = {'message': "Review added successfully!!"}
            resp = jsonify(message)
            resp.status_code = 200
            return resp

    """Get all reviews of a business"""
    @token_required
    @swag_from("../APIdocs/AddReview.yml")
    def get(self, bizid):
        """Gets all reviews added to a specified business"""

        business = Business.query.get(bizid)
        if not business:
            message = {'message': "Business doesn't exist!!"}
            resp = jsonify(message)
            resp.status_code = 404

        reviews = Review.query.filter_by(business_id=bizid).all()
        if not reviews:   
            message = {'message': "Business doesn't have reviews yet!!"}
            resp = jsonify(message)
            resp.status_code = 404
       
        output = []
        for rev in reviews:
            review_item = {
                'review message': rev.review_msg,
                'business ID': rev.business_id,
                'Reviewd by': rev.user_id
                 }
            output.append(review_item)
            message = {'Reviews': output}
            resp = jsonify(message)
            resp.status_code = 200
        return resp
        