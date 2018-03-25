from resources.resources import app, SQLAlchemy

db = SQLAlchemy(app)
db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    userEmail = db.Column(db.String(60), unique=True)
    userPassword = db.Column(db.String(300))
    user_name = db.Column(db.String(60))
    businesses = db.relationship('Business', backref='user',
                                 lazy='dynamic')
    def __init__(self, userEmail, userPassword):
        self.user_email = userEmail#pragma:no cover
        self.userPassword = userPassword#pragma:no cover
        db.create_all()   #pragma:no cover
    
class Business(db.Model):
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)
    businessName = db.Column(db.String(60), nullable=False, unique=True)
    businessProfile = db.Column(db.String(1000), nullable=False)
    location = db.Column(db.String(200))
    category = db.Column(db.String(200))
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviews = db.relationship('Review', backref='business',
                                 lazy='dynamic')
    def __init__(self, businessName, businessProfile, location, category, userID):
        self.businessName = businessName#pragma:no cover
        self.businessProfile = businessProfile#pragma:no cover
        self.location = location
        self.category = category
        self.userID = userID
        db.create_all()#pragma:no cover

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    reviewMsg = db.Column(db.String(1000), nullable=False)
    businessID = db.Column(db.Integer, db.ForeignKey('businesses.id'))
    def __init__(self, reviewMsg, businessID):
        self.reviewMsg = reviewMsg#pragma:no cover
        self.businessID = businessID
        db.create_all()#pragma:no cover
