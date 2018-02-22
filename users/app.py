from resources.lib import *
from resources.userAPI import UserRegister, UserLogin, UserLogout




api.add_resource(UserRegister, '/api/v1/auth/register')
api.add_resource(UserLogin, '/api/v1/auth/login')
api.add_resource(UserLogout, '/api/v1/auth/logout')

if __name__ == '__main__':
    app.run(debug=True)