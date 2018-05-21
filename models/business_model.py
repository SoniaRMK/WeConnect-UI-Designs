from resources import app, db
from werkzeug.security import generate_password_hash
from flask import jsonify

class Business(db.Model):
    """Model to create a business"""

    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_name = db.Column(db.String(60), nullable=False, unique=True)
    business_profile = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(60), nullable=False)
    category = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())
    reviews = db.relationship('Review', backref='business', lazy='dynamic')
    def __init__(self, business_name, business_profile, location, category, user_id):
        self.business_name = business_name
        self.business_profile = business_profile
        self.location = location
        self.category = category
        self.user_id = user_id
        db.create_all()

    @staticmethod
    def businesses_to_json(businesses):
        """Returns businesses in a JSON format"""
        businesses_results = []
        for business in businesses:
            output = {
                'Business Name': business.business_name,
                'Business Profile': business.business_profile,
                'Location': business.location,
                'Category': business.category
                }
            businesses_results.append(output)
        return businesses_results

    @staticmethod
    def businesses_found_message(businesses):
        message = {'Businesses': businesses}
        resp = jsonify(message)
        resp.status_code = 200
        return resp

    @staticmethod
    def limit_less_zero(limit):
        """Return Message when Limit is 0 or negative"""
        if limit <=0 or isinstance(limit,str): 
            message = {'message': 'Limit should be a positive integer greater than 0'}
            resp = jsonify(message)
            resp.status_code = 400
            return resp

    @staticmethod
    def search_businesses(search_term="", location="", category="", limit=10):
        """Searches for businesses based on the parameters provided by the user"""
        if search_term is not None:
            """search for business based on a search term q"""
            businesses = Business.query.filter(Business.business_name.ilike("%{}%".format(search_term)))
            if location is not None and category is None and limit is None:
                """filter businesses based on location"""
                businesses = businesses.filter(Business.location.ilike("%{}%".format(location))).all()
                businesses = Business.businesses_to_json(businesses)
                response = Business.businesses_found_message(businesses)
                return response
            elif category is not None and location is None and limit is None:
                """filter businesses based on category"""
                businesses = businesses.filter(Business.category.ilike("%{}%".format(category))).all()
                businesses = Business.businesses_to_json(businesses)
                response = Business.businesses_found_message(businesses)
                return response
            elif category is not None and location is not None and limit is None:
                """ filter business based on location and category"""
                businesses = businesses.filter(Business.location.ilike("%{}%".format(location)))
                businesses = businesses.filter(Business.category.ilike("%{}%".format(category))).all()
                businesses = Business.businesses_to_json(businesses)
                response = Business.businesses_found_message(businesses)
                return response
            elif category is not None and limit is not None and location is None:
                """Search for business based on category and limit is given"""
                businesses = businesses.filter(Business.category.ilike("%{}%".format(category)))
                try:
                    if limit <= 0:
                        response = Business.limit_less_zero(limit)
                        return response
                    businesses = businesses.paginate(per_page=limit, page=1, error_out=True).items
                    businesses = Business.businesses_to_json(businesses)
                    response = Business.businesses_found_message(businesses)
                    return response
                except ValueError:
                    response = Business.limit_less_zero(limit)
                    return response
            elif location is not None and limit is not None and category is None:
                """ search for business based on location"""
                businesses = businesses.filter(Business.location.ilike("%{}%".format(location)))
                try:
                    if limit <= 0:
                        response = Business.limit_less_zero(limit)
                        return response
                    businesses = businesses.paginate(page=1, per_page=limit, error_out=True).items
                    businesses = Business.businesses_to_json(businesses)
                    response = Business.businesses_found_message(businesses)
                    return response
                except ValueError:
                    response = Business.limit_less_zero(limit)
                    return response
            elif location is not None and limit is not None and category is not None:
                """search for business based on location and category and limit results per page"""
                businesses = businesses.filter(Business.location.ilike("%{}%".format(location)))
                businesses_result = businesses.filter(Business.category.ilike("%{}%".format(category)))
                try:
                    if limit <= 0:
                        response = Business.limit_less_zero(limit)
                        return response
                    businesses = businesses_result.paginate(per_page=limit, page=1, error_out=True).items
                    businesses = Business.businesses_to_json(businesses)
                    response = Business.businesses_found_message(businesses)
                    return response
                except ValueError:
                    response = Business.limit_less_zero(limit)
                    return response
            elif limit is not None and location is None and category is None:
                """ limit number of businesses per page"""
                try:
                    if limit <= 0:
                        response = Business.limit_less_zero(limit)
                        return response
                    businesses = businesses.paginate(per_page=limit, page=1, error_out=True).items
                    businesses = Business.businesses_to_json(businesses)
                    response = Business.businesses_found_message(businesses)
                    return response
                except ValueError:
                    response = Business.limit_less_zero(limit)
                    return response
            else:
                businesses = Business.businesses_to_json(businesses)
                response = Business.businesses_found_message(businesses)
                return response
        else:
            """Get all businesses"""
            businesses = Business.query.all()
            if limit is not None:
                try:
                    if limit <= 0 or isinstance(limit,str):
                        response = Business.limit_less_zero(limit)
                        return response
                    businesses = Business.query.paginate(per_page=limit, page=1, error_out=True).items
                    businesses = Business.businesses_to_json(businesses)
                    response = Business.businesses_found_message(businesses)
                    return response
                except ValueError:
                    response = Business.limit_less_zero(limit)
                    return response
            businesses = Business.businesses_to_json(businesses)
            response = Business.businesses_found_message(businesses)
            return response
