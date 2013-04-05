import os

class Config(object):
    DEBUG = False
    TESTING = False
    MONGO_HOST = 'localhost'
    SECRET_KEY = os.urandom(24)
    MONGO_DATABASE = 'floto'

class ProductionConfig(Config):
    APPLICATION_ROOT = '/floto/api'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    MONGO_DATABASE = 'test'