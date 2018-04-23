from flask import jsonify
from flask_restful.reqparse import RequestParser
from models.models import Business


q_request_parser = RequestParser(bundle_errors=True)
q_request_parser.add_argument("q", type=str, required=False, help="Search business by name")

def search_by_name(q):
    """search for businesses based on a search parameter q"""
    business_search_result = Business.query.order_by(
        Business.business_name).filter(Business.business_name.like('%' + q + '%'))
    business_list=[]

    if not business_search_result:
        message = {
                'status': "Not Found",
                'message': 'No Businesses found!',
                }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    
    for business in business_search_result:
        output = {
            'Business Name': business.business_name,
            'Business Profile': business.business_profile,
            'Location': business.location,
            'Category': business.category
            }
        business_list.append(output)

    return jsonify({'businesses': business_list})   
 
def filter_by_category(business_category):
    """Filter businesses based on category"""
    business_filter_result = Business.query.filter_by(category=business_category).all()
    businesses = []
    if not business_filter_result:
        message = {
                'status': "Not Found",
                'message': 'No Businesses found!',
                }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
        
    for business in business_filter_result:
        output = {
                'Business Name': business.business_name,
                'Business Profile': business.business_profile,
                'Location': business.location,
                'Category': business.category
                }
        businesses.append(output)
    return jsonify({'Businesses': businesses})

def filter_by_location(business_location):
    """Filter businesses based on location"""
    business_filter_result = Business.query.filter_by(location=business_location).all()
    businesses = []
    if not business_filter_result:
        message = {
                'status': "Not Found",
                'message': 'No Businesses found!',
                }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
        
    for business in business_filter_result:
        output = {
                'Business Name': business.business_name,
                'Business Profile': business.business_profile,
                'Location': business.location,
                'Category': business.category
                }
        businesses.append(output)
    return jsonify({'Businesses': businesses})