import sys
sys.path.append('..')
from resources import *
from resources.business_api import businesses
from flask_restful.reqparse import RequestParser


reviews = []

#Validating the arguments
review_validation = RequestParser(bundle_errors=True)
review_validation.add_argument("reviewMsg", type=str, required=True, help="Review Message should be a string")

class Review(Resource):
    @swag_from("../APIdocs/ViewReviews.yml")
    #Add a review to a business
    def post(self, bizid):
        review_args = review_validation.parse_args()  

        business = [busi for busi in businesses if busi['businessID'] == bizid]
        review = {
                'reviewMsg': review_args.reviewMsg, 
                'businessID': bizid,                    
                'createdBy': 'Sonia',
                }
        if business != []:
            reviews.append(review)
            message = {
                    'status': review,
                    'message': "Review added successfully!!",
                    }
            resp = jsonify(message)
            resp.status_code = 200
        else:
            message = {
                    'status': "Not Found",
                    'message': "Can't add review. Business not registered yet!!",
                    }
            resp = jsonify(message)
            resp.status_code = 404
        
        return resp
    #Get all reviews of a business
    @swag_from("../APIdocs/AddReview.yml")
    def get(self, bizid):
        business = [busi for busi in businesses if busi['businessID'] == bizid]
        reviewsbiz = [rev for rev in reviews if rev['businessID'] == bizid]
        if business and reviewsbiz:
            message = {
                'status': "Success",
                'Reviews': reviewsbiz,
            }
            resp = jsonify(message)
            resp.status_code = 200
        elif business and not reviewsbiz:   
            message = {
                    'status': "Not Found",
                    'message': "Business doesn't have reviews yet!!",
                }
            resp = jsonify(message)
            resp.status_code = 404
        else:
            message = {
                'status': "Not Found",
                'message': "Business doesn't exist!!",
            }
            resp = jsonify(message)
            resp.status_code = 404
        return resp