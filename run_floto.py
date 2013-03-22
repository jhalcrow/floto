#!/usr/bin/env python2.7

from floto import create_app

app = create_app()
app.run('0.0.0.0', port=5100, debug=True)