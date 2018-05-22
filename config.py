class Config(object):
    TESTING = False
    DEBUG = False
    CSRF_ENABLED = True  # protect against CSRF attacks
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Oxa34KLncvfjKEjXkf'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SWAGGER_UI_JSONEDITOR = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234567890@localhost/testdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234567890@localhost/testdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}