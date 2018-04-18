import sys
sys.path.append('..')
from resources import *
from resources.user_api import UserRegister, UserLogin, UserLogout, UserResetPassword
from resources.business_api import BusinessList, Business
from resources.review_api import Review


api.add_resource(UserRegister, '/api/v1/auth/register')
api.add_resource(UserLogin, '/api/v1/auth/login')
api.add_resource(UserLogout, '/api/v1/auth/logout')
api.add_resource(UserResetPassword, '/api/v1/auth/reset-password')
api.add_resource(BusinessList, '/api/v1/businesses')
api.add_resource(Business, '/api/v1/businesses/<int:bizid>')
api.add_resource(Review, '/api/v1/businesses/<int:bizid>/reviews')

if __name__ == '__main__':
    app.run(debug=True)