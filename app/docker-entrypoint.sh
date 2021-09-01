#!/bin/sh
# set -e
flask db init
flask db migrate 
flask db upgrade
# run tests
# bind to 5000 port
gunicorn  --bind=0.0.0.0:5000 app.main:app 