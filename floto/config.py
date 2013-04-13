import os

class Config(object):
    DEBUG = False
    TESTING = False
    MONGO_HOST = 'localhost'
    SECRET_KEY = os.urandom(24)
    MONGO_DATABASE = 'floto'
    API_PREFIX = None

class ProductionConfig(Config):
    APPLICATION_ROOT = '/floto/api'

class DevelopmentConfig(Config):
    DEBUG = True
    API_PREFIX='/floto/api'

class TestingConfig(Config):
    TESTING = True
    MONGO_DATABASE = 'test'
    API_PREFIX='/floto/api'