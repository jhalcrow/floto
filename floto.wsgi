#!/usr/bin/python

import os
import sys
import logging
logging.basicConfig(stream=sys.stderr)
# virtualenv activation if any
#activate_this = '/home/envs/supaenv/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from floto import create_app, config
application = create_app(config.ProductionConfig())

from logging.handlers import FileHandler
file_handler = FileHandler('/tmp/floto.log')

file_handler.setLevel(logging.DEBUG)
application.logger.addHandler(file_handler)
