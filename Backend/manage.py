"""
**Manage.py is the starting point**: the application script where the instance is defined.

The configuration used to create the instance can be defined in a .env file as FLASK_ENV ('flask environment'), which can be "local", "development", or "production". In the case you do not have a .env, a local instance will be created using values from the .env.default file. This file can also be used as an example for creating a .env file.

The configuration files can be found inside the config directory. The appropriate one will be selected according to the value set to FLASK_ENV and passed on to the create_app application factory inside app/__init__.py

Note about ip-address and related functions: remote_addr will be 127.0.0.1 in dev MODE, which means the ip-geolocation will be useless (in the stats module)

ENVIRONMENT_OPTIONS = ["local", "development", "production"] -> *set in values_setter*
"""
import os
from app import create_app
from app.extensions.extensions import db 
from config.config_dev import DevelopmentConfig
from config.config_prod import ProductionConfig
from config.values import ENVIRONMENT
from scripts.setup import initial_setup

# When "local" or "development" environments are set, this file will run an extra script:
# - Dummie data will populate the database using the content from "seed"
# - It will be checked whether redis is running
# When "development" environment is set, this file will run an extra script:
# - Check whether there is a .env file and warn in case the data in this file is incorrect


if ENVIRONMENT == "local" or ENVIRONMENT == "development":
    app = create_app(DevelopmentConfig)
else:
    SHOW_WARNINGS = False # --> ?
    app = create_app(ProductionConfig)

with app.app_context():
    db.create_all()
    initial_setup(ENVIRONMENT)

# The code bellow will run with every API used to log the session data. It can be used for debugging authorization errors.
# from flask import session, request
# from flask_login import current_user
# from app.utils.console_warning.print_warning import console_warn
# @app.before_request
# def debug_sessions():
#     if MODE == "dev":  # Only log in development mode
#         console_warn(f"Session debugging:", "BLUE")
#         console_warn(f"     Session data: {session}", "WHITE")
#         console_warn(f"     Session type: {type(session)}", "WHITE")
#         console_warn(f"     Current user authenticated: {current_user.is_authenticated}", "WHITE")
        
#         if "_SD_session" not in request.cookies:
#             console_warn(f"     No session cookie sent. Browser blocked?", "RED")

if __name__ == "__main__":
    if ENVIRONMENT == "local" or ENVIRONMENT == "development":
        from utils.print_to_terminal import print_to_terminal
        print_to_terminal(f"App running in HTTP: {ENVIRONMENT} environment", "BLUE")
        app.run(debug=True)
    else:
        app.run() # set accordingly for production. 
        #Eg: if using waitress something like: serve(app, host='0.0.0.0', port=5000, threads=4)