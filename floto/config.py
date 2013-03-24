import os

class Config(object):
    DEBUG = False
    TESTING = False
    MONGO_HOST = 'localhost'
    SECRET_KEY = os.urandom(24)

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True