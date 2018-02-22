from resources.lib import *
from resources.userAPI import UserRegister, UserLogin, UserLogout
from resources.businessAPI import BusinessList, Business
from resources.reviewAPI import Review


api.add_resource(UserRegister, '/api/v2/auth/register')
api.add_resource(UserLogin, '/api/v2/auth/login')
api.add_resource(UserLogout, '/api/v2/auth/logout')
api.add_resource(BusinessList, '/api/v2/businesses')
api.add_resource(Business, '/api/v2/businesses/<int:bizid>')
api.add_resource(Review, '/api/v2/businesses/<int:bizid>/reviews')

if __name__ == '__main__':
    app.run(debug=True)