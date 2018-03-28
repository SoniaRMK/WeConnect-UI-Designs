from .resources import *
from flask_restful.reqparse import RequestParser
from models.models import Business


#Validating the arguments
business_validation = RequestParser(bundle_errors=True)
business_validation.add_argument("business_name", type=str, required=True, help="Business Name must be a string")
business_validation.add_argument("category", type=str, required=True, help="Category must be a string")
business_validation.add_argument("location", type=str, required=True, help="Location must be a string")
business_validation.add_argument("business_profile", type=str, required=True, help="Business Profile must be a string")


class Business(Resource):
    #gets a  business
    @swag_from("../APIdocs/ViewBusiness.yml")
    @token_required
    def get(self, bizid):
        business = Business.query.filter_by(id=bizid).first()
        if not business:
            message = {
                'status': "Not Found",
                'message': 'Business not registered yet!',
                }
            resp = jsonify(message)
            resp.status_code = 404
            return resp

        output = {}
        output['Business Name'] = business.business_name
        output['Business Profile'] = business.business_profile
        output['Location'] = business.location
        output['Category'] = business.category
        
        return jsonify({'business': output})

    #deletes a business
    @swag_from("../APIdocs/DeleteBusiness.yml")
    @token_required
    def delete(self, bizid):
        userid = request.data['user']
        business = Business.query.filter_by(id=bizid).first()
        if business.user_id != userid:
            message = {
            'status': "Unathorized",
            'message': "You cannot delete a business you didn't register!!",
            }
            resp = jsonify(message)
            resp.status_code = 401
        if not business:
            message = {
                'status': "Not Found",
                'message': 'Business not registered yet!',
                }
            resp = jsonify(message)
            resp.status_code = 404
            return resp

        db.session.delete(business)
        db.session.commit()

        message = {
            'status': "Success",
            'message': 'Business successfully Deleted!',
            }
        resp = jsonify(message)
        resp.status_code = 200
        return resp
        
    #edits a  business
    @swag_from("../APIdocs/UpdateBusiness.yml")
    @token_required
    def put(self, bizid):
        userid = request.data['user']
        business = Business.query.filter_by(id=bizid).first()
        if business.user_id != userid:
            message = {
            'status': "Unathorized",
            'message': "You cannot Edit a business you didn't register!!",
            }
            resp = jsonify(message)
            resp.status_code = 401
        if not business:
            message = {
                'status': "Not Found",
                'message': 'Business not registered yet!',
                }
            resp = jsonify(message)
            resp.status_code = 404
            return resp
        business.business_name = data['new_name']
        business.business_profile = data['new_description']
        business.location = data['new_location']
        business.category = data['new_category']
        message = {
            'status': "Success",
            'message': 'Business successfully Updated!',
            }
        resp = jsonify(message)
        resp.status_code = 200
        return resp
        

class BusinessList(Resource):
    #creates a new business
    @swag_from("../APIdocs/CreateBusiness.yml")
    @token_required
    def post(self):
        user = request.data['user']
        business = Business(business_name=business_validation.parse_args().business_name, 
                            category=business_validation.parse_args().category,
                            location=business_validation.parse_args().location,
                            business_profile=business_validation.parse_args().business_profile)
                            #user_id=user)

        try:
            #user = models.User(user_email, user_password)
            db.session.add(business)
            db.session.commit()
            message = {
                'status': "Success",
                'message': 'Business registered!',
                }
            resp = jsonify(message)
            resp.status_code = 201
        except:
            message = {
                'status': "Conflict",
                'message': 'Business already Exists!',
                }
            resp = jsonify(message)
            resp.status_code = 409 
        
        db.session.close()
        return resp 
    
    #Get all businesses
    @swag_from("../APIdocs/ViewBusinesses.yml")
    @token_required
    def get(self):
        businesses = Business.query.all()
        if not businesses:
            message = {
                'status': "Not Found",
                'message': 'No businesses found!',
                }
            resp = jsonify(message)
            resp.status_code = 404
            return resp

        business_list=[]
        for business in business_list:
            output={}
            output['Business Name'] = business.business_name
            output['Business Profile'] = business.business_profile
            output['Location'] = business.location
            output['Category'] = business.category
            business_list.append(output)
        return jsonify({'businesses': business_list})