import os
from flask import Flask
from floto.api import api
import pymongo
import boto


def s3_setup(app):
   
    s3 = boto.connect_s3(
        app.config['AWS_ACCESS_KEY_ID'],
        app.config['AWS_SECRET_ACCESS_KEY']
    )

    bucket = s3.create_bucket(app.config['S3_BUCKET'])
    return s3, bucket

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
 
    s3, bucket = s3_setup(app)
    app.extensions['s3_bucket'] = bucket
    app.extensions['s3'] = s3

    return app