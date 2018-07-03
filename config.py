import os

class Config(object):
    TESTING = False
    DEBUG = False
    CSRF_ENABLED = True  # protect against CSRF attacks
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Oxa34KLncvfjKEjXkf'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql://postgres:1234567890@localhost/weconnect')


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SWAGGER_UI_JSONEDITOR = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    