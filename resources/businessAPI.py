from resources.lib import *
from flask_restful.reqparse import RequestParser

businesses = []

#Validating the arguments
business_validation = RequestParser(bundle_errors=True)
business_validation.add_argument("businessName", type=str, required=True, help="Business Name must be a string")
business_validation.add_argument("Category", type=str, required=True, help="Category must be a string")
business_validation.add_argument("Location", type=str, required=True, help="Location must be a string")
business_validation.add_argument("businessProfile", type=str, required=True, help="Business Profile must be a string")


class Business(Resource):
    #gets a  business
    @token_required
    def get(self, bizid):
        biz = [business for business in businesses if business['businessID'] == bizid]
        if biz == []:
            message = {
            'status': "Not Found",
            'message': 'Business Not registered yet!!',
            }
            resp = jsonify(message)
            resp.status_code = 404
        else:
            message = {
            'status': "Success",
            'business': biz[0],
            }
            resp = jsonify(message)
            resp.status_code = 200

        return resp

    #deletes a business
    @token_required
    def delete(self, bizid):
        biz = [business for business in businesses if business['businessID']==bizid]
        if biz == []:
            message = {
            'status': "Not Found",
            'message': 'Business Not registered yet!!',
            }
            resp = jsonify(message)
            resp.status_code = 404
        else:
            businesses.remove(biz[0])
            message = {
                'status': "success",
                'message': 'Successfully Deleted!!',
            }
            resp = jsonify(message)
            resp.status_code = 200

        return resp
        
    #edits a  business
    @token_required
    def put(self, bizid):
        business_args = business_validation.parse_args() 
        biz = [business for business in businesses if business['businessID'] == bizid]
        biz[0]['businessName'] = business_args.businessName
        biz[0]['businessProfile'] = business_args.businessProfile
        biz[0]['Category'] = business_args.Category
        biz[0]['Location'] = business_args.Location
        business = [busi for busi in businesses if business_args.businessName == busi['businessName'] and business_args.Category == busi['Category']]
        if len(business) > 1:
            message = {
                    'status': "Failed",
                    'message': 'Business Already Exists!',
                    }
            resp = jsonify(message)
            resp.status_code = 400
        else:
            message = {
            'status': "Success",
            'message': 'Business successfully Edited!',
            }
            resp = jsonify(message)
            resp.status_code = 400

        return resp
       # message = "Business successfully Edited!"
        
        #return jsonify({'Message': message}), 200

class BusinessList(Resource):
    #creates a new business
    @token_required
    def post(self):
        business_args = business_validation.parse_args() 
        biz = {
        'businessID' : len(businesses)+ 1,
        'businessName' : business_args.businessName,
        'Location' : business_args.Location, 
        'Category' : business_args.Category, 
        'businessProfile': business_args.businessProfile, 
        'createdBy': request.data['user'],
        #'createdOn' : datetime.date
        }
        business = [busi for busi in businesses if request.json['businessName'] == busi['businessName'] and request.json['Category'] == busi['Category']]
        if len(business) == 0:
            businesses.append(biz)
            message = {
            'status': "success",
            'message': 'Business Successfully Created!!',
            }
            resp = jsonify(message)
            resp.status_code = 200
      
        else:
            message = {
            'status': "Failed",
            'message': 'Business Already Created!',
            }
            resp = jsonify(message)
            resp.status_code = 400

        return resp
    
    #Get all businesses
    @token_required
    def get(self):
        return jsonify({'businesses': businesses})