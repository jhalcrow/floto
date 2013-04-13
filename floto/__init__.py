import os
from flask import Flask
from floto.api import api
import pymongo

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    if 'FLOTO_CONFIG' in os.environ:
        app.config.from_envvar('FLOTO_CONFIG')
    api_prefix = app.config['API_PREFIX']

    app.register_blueprint(api, url_prefix=api_prefix)
    if not app.extensions:
        app.extensions = {}

    app.extensions['mongo'] = pymongo.Connection(app.config['MONGO_HOST'])[app.config['MONGO_DATABASE']]

    return app