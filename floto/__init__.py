from flask import Flask
from floto.api import api

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)

    return app