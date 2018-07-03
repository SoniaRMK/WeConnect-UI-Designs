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
    reviews = db.relationship('Review', backref='business', lazy='dynamic', 
                            cascade="all, delete-orphan")
    
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
                'BusinessName': business.business_name,
                'BusinessProfile': business.business_profile,
                'Location': business.location,
                'Category': business.category, 
                'CreatedBy' : username,
                'id' : business.id
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
        """Return Message when no business is found""" 
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
    def search_businesses(search_term="", location="", category="", page=1):
        """Searches for businesses based on the parameters provided by the user"""
        if search_term:
            """search for business based on a search term q"""
            businesses = Business.query.filter(Business.\
                         business_name.ilike("%{}%".format(search_term))).order_by(Business.created_at)
        else:
            businesses = Business.query.order_by(Business.created_at)  
        if category:
            """filter businesses based on category"""
            businesses = businesses.filter(Business.\
                         category.ilike("%{}%".format(category)))        
        if location:
            """filter businesses based on location"""
            businesses = businesses.filter(Business.\
                         location.ilike("%{}%".format(location)))

        businesses_list = businesses.paginate(per_page=2, page=page, error_out=False)
        businesses = businesses_list.items
        next_page = businesses_list.next_num if businesses_list.has_next else None
        prev_page = businesses_list.prev_num if businesses_list.has_prev else None
        businesses = Business.businesses_to_json(businesses)
        message = {'Businesses': businesses, 
                   'prevPage': prev_page, 
                   'nextPage' : next_page
                }
        response = jsonify(message)
        response.status_code = 200
        if len(businesses) == 0:
            response = Business.businesses_not_found_message(businesses)
        return response
