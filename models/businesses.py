from resources import app, db
from flask import jsonify
from models.users import User

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
    
    def __init__(self, business_name, business_profile,\
                 location, category, user_id):
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
            userid = business.user_id
            user = User.query.filter_by(id=userid).first()
            username = user.user_name
            output = {
                'Business Name': business.business_name,
                'Business Profile': business.business_profile,
                'Location': business.location,
                'Category': business.category, 
                'Created By' : username
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
    def businesses_not_found_message(businesses):
        """Return Message when Limit is 0 or negative""" 
        message = {'message': 'No businesses found'}
        resp = jsonify(message)
        resp.status_code = 404
        return resp

    @staticmethod
    def limit_less_zero(limit):
        """Return Message when Limit is 0 or negative"""
        if limit <=0: 
            message = {'message': 'Limit should be a positive integer greater than 0'}
            resp = jsonify(message)
            resp.status_code = 403
            return resp
        
    @staticmethod
    def search_businesses(search_term="", location="", category="", limit=10):
        """Searches for businesses based on the parameters provided by the user"""

        if search_term is not None:
            """search for business based on a search term q"""
            businesses = Business.query.filter(Business.\
                         business_name.ilike("%{}%".format(search_term)))
        else:
            businesses = Business.query.order_by(Business.business_name)           
        if location is not None:
            """filter businesses based on location"""
            businesses = businesses.filter(Business.\
                         location.ilike("%{}%".format(location))).all()
            businesses = Business.businesses_to_json(businesses)
            response = Business.businesses_found_message(businesses)
            if len(businesses)==0:
                response = Business.businesses_not_found_message(businesses)
            return response
        if category is not None:
            """filter businesses based on category"""
            businesses = businesses.filter(Business.\
                         category.ilike("%{}%".format(category))).all()
            businesses = Business.businesses_to_json(businesses)
            response = Business.businesses_found_message(businesses)
            if len(businesses)==0:
                response = Business.businesses_not_found_message(businesses)
            return response
        if limit is not None:
            """ limit number of businesses per page"""
            if limit <= 0:
                response = Business.limit_less_zero(limit)
            else:
                businesses = businesses.paginate(per_page=limit, page=1, error_out=True).items
                businesses = Business.businesses_to_json(businesses)
                response = Business.businesses_found_message(businesses)
                if len(businesses) == 0:
                    response = Business.businesses_not_found_message(businesses)
            return response
        businesses = Business.businesses_to_json(businesses)
        response = Business.businesses_found_message(businesses)
        if len(businesses) == 0:
            response = Business.businesses_not_found_message(businesses)
        return response
