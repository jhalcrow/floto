from flask import Flask
from floto.api import api
import pymongo

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)
    if not app.extensions:
        app.extensions = {}

    app.extensions['mongo'] = pymongo.Connection().floto

    return app