from resources import *
from flask_restful.reqparse import RequestParser
from models.models import Business


#Validating the arguments
business_validation = RequestParser(bundle_errors=True)
business_validation.add_argument("business_name", type=str, required=True, help="Business Name must be a string")
business_validation.add_argument("category", type=str, required=True, help="Category must be a string")
business_validation.add_argument("location", type=str, required=True, help="Location must be a string")
business_validation.add_argument("business_profile", type=str, required=True, help="Business Profile must be a string")

#Validating search by name q and filtering by location and category
q_request_parser = RequestParser(bundle_errors=True)
q_request_parser.add_argument("q", type=str, required=False, help="Search term missing")
q_request_parser.add_argument("limit", type=int, required=False, help="Businesses results limit missing")
q_request_parser.add_argument( "page", type=int, required=False, help="Businesses results page to view missing")
q_request_parser.add_argument("location", type=str, required=False, help="Business location filter missing")
q_request_parser.add_argument("category", type=str, required=False, help="Business category filter missing")

class BusinessOne(Resource):
    """Class for getting, updating and deleting a business"""

    @swag_from("../APIdocs/ViewBusiness.yml")
    @token_required
    def get(self, bizid):
        """gets a  business"""
        business = Business.query.get(bizid)
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
        business = Business.query.get(bizid)
        if business is None:
            message = {
                'status': "Not Found",
                'message': 'Business not registered yet!',
                }
            resp = jsonify(message)
            resp.status_code = 404
            return resp
        if business.user_id != userid:
            message = {
            'status': "Unathorized",
            'message': "You cannot delete a business you didn't register!!",
            }
            resp = jsonify(message)
            resp.status_code = 401
            return resp
        else:
            db.session.delete(business)
            #db.session.commit()
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
        if not business:
            message = {
                'status': "Not Found",
                'message': 'Business not registered yet!',
                }
            resp = jsonify(message)
            resp.status_code = 404
            return resp
        if business.user_id != userid:
            message = {
            'status': "Unathorized",
            'message': "You cannot Edit a business you didn't register!!",
            }
            resp = jsonify(message)
            resp.status_code = 401

        business.business_name=business_validation.parse_args().business_name
        business.business_profile=business_validation.parse_args().business_profile
        business.location=business_validation.parse_args().location
        business.category=business_validation.parse_args().category
        db.session.commit()
        message = {
            'status': "Success",
            'message': 'Business successfully Updated!',
            }
        resp = jsonify(message)
        resp.status_code = 200
        return resp
        

class BusinessList(Resource):
    """class to create a business and get all businesses""" 
    @swag_from("../APIdocs/CreateBusiness.yml")
    @token_required
    def post(self):
        """creates a new business"""

        user = request.data['user']
        business = Business(
            business_name=business_validation.parse_args().business_name,
            business_profile=business_validation.parse_args().business_profile, 
            location=business_validation.parse_args().location, 
            category=business_validation.parse_args().category,
            user_id=user)

        try:
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
    
    @swag_from("../APIdocs/ViewBusinesses.yml")
    def get(self):
        """Get all businesses registered"""
        args = q_request_parser.parse_args()
        q = args.get('q', None)
        limit = args.get('limit', 10)
        page = args.get('page', 1)
        location_name = args.get('location', None)
        category_name = args.get('category', None)

        if q:
            q = q.lower()
            businesses_result = Business.query.order_by(Business.business_name).filter(Business.business_name.ilike('%' + q + '%'))
        else:
            businesses_result = Business.query.order_by(Business.business_name)
    
        if location_name:
            businesses_result= Business.query.filter(Business.location.ilike('%'+location_name+'%'))

        if category_name:
            businesses_result= Business.query.filter(Business.category.ilike('%'+category_name+'%'))

        businesses_result = businesses_result.paginate(page=page, per_page=limit, error_out=False)
        
        businesses = businesses_result.items

        business_list=[business.business_as_dict()
                           for business in businesses]
        if businesses is None:
            message = {
                'status': "Not Found",
                'message': 'No businesses found!',
                }
            resp = jsonify(message)
            resp.status_code = 404
            return resp
        
        for business in businesses:
            output = {
                'Business Name': business.business_name,
                'Business Profile': business.business_profile,
                'Location': business.location,
                'Category': business.category
                }
            business_list.append(output)

        next_page = businesses_result.next_num if businesses_result.has_next else None
        prev_page = businesses_result.prev_num if businesses_result.has_prev else None
        
        business_returned = {'businesses': business_list, "next_page": next_page, "prev_page": prev_page}
        resp = jsonify(business_returned)
        resp.status_code = 200
        return resp