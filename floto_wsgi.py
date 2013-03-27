#!/usr/bin/python

import os
import sys
import logging
# virtualenv activation if any
#activate_this = '/home/envs/supaenv/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from floto import create_app, config
application = create_app(config.DevelopmentConfig())
from werkzeug.contrib.fixers import ProxyFix
application.wsgi_app = ProxyFix(application.wsgi_app)

@application.before_first_request
def setup_logging():
    # In production mode, add log handler to sys.stderr.
    application.logger.addHandler(logging.StreamHandler())
    application.logger.setLevel(logging.DEBUG)
    application.logger.addHandler(logging.FileHandler('/tmp/floto.log'))

#from logging.handlers import FileHandler
#file_handler = FileHandler('/tmp/floto.log')

#file_handler.setLevel(logging.DEBUG)
#application.logger.addHandler(file_handler
sys.stderr.write("WTF\n")
