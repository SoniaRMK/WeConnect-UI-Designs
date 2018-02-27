from resources.lib import *
from resources.businessAPI import businesses


reviews = []

class Review(Resource):
    #Add a review to a business
    def post(self, bizid):
        business = [busi for busi in businesses if busi['businessID'] == bizid]
        if business != []:
            review = {
                    'reviewMsg': request.json['reviewMsg'], 
                    'businessID': bizid,
                    # 'CreatedBy' : request.json['userEmail'],
                    # 'userID' : 
                    }
            reviews.append(review)
            message = {
                    'status': "Success!",
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
    def get(self, bizid):
        business = [busi for busi in businesses if busi['businessID'] == bizid]
        reviewsbiz = [rev for rev in reviews if rev['businessID'] == bizid]
        if business != [] and reviewsbiz != []:
            message = {
                'status': "Success",
                'Reviews': reviewsbiz,
            }
            resp = jsonify(message)
            resp.status_code = 200
        elif business != [] and reviewsbiz == []:   
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