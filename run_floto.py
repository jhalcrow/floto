#!/usr/bin/env python2.7

from floto import create_app, config

app = create_app()
app.config.from_object(config.DevelopmentConfig())
app.run('0.0.0.0', port=5100, debug=True)