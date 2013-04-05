from flask import Flask
from floto.api import api
import pymongo

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config.from_envvar('FLOTO_CONFIG')
    app.register_blueprint(api)
    if not app.extensions:
        app.extensions = {}

    app.extensions['mongo'] = pymongo.Connection(app.config['MONGO_HOST'])[app.config['MONGO_DATABASE']]

    return app