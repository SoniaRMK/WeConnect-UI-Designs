class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'Oxa34KLncvfjKEjXkf'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SWAGGER_UI_JSONEDITOR = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234567890@localhost/weconnect'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234567890@localhost/testdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    