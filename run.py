from resources import *
from resources.user_api import UserRegister, UserLogin, UserLogout, UserResetPassword
from resources.business_api import BusinessList, BusinessOne
from resources.review_api import ReviewBusiness


api.add_resource(UserRegister, '/api/v2/auth/register')
api.add_resource(UserResetPassword, '/api/v2/auth/reset-password')
api.add_resource(UserLogin, '/api/v2/auth/login')
api.add_resource(UserLogout, '/api/v2/auth/logout')
api.add_resource(BusinessList, '/api/v2/businesses')
api.add_resource(BusinessOne, '/api/v2/businesses/<int:bizid>')
api.add_resource(ReviewBusiness, '/api/v2/businesses/<int:bizid>/reviews')

if __name__ == '__main__':
    app.run(debug=True)