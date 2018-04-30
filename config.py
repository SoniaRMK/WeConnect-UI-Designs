"""Weconnect API configurations"""

class Config(object):
    """Common Configurations"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'Oxa34KLncvfjKEjXkf'
    CSRF_ENABLED = True  # protect against CSRF attacks


class DevelopmentConfig(Config):
    """Development configurations"""
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234567890@localhost/WeConnect'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    """Production configurations"""
    DEBUG = False


class TestingConfig(Config):
    """Testing Configurations"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234567890@localhost/testdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
