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
# - SSL certificates will be generated (and used)
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
        # If an SSL certificate and key are available in the specified folder, they will be used to build an HTTP connection. This is recommended.
        if os.path.exists(os.path.join(os.getcwd(), "certs")) and os.listdir(os.path.join(os.getcwd(), "certs")):
            # print_to_terminal(f"App running in HTTPS: be sure to check front end path.", "BLUE")
            app.run(ssl_context=("certs/cert.pem", "certs/key.pem"), debug=(ENVIRONMENT == "development"))
        else:
            # print_to_terminal(f"App running in HTTP: be sure to check front end path.", "BLUE")
            app.run(debug=(ENVIRONMENT == "development"))
    else:
        app.run() # set accordingly for production. 
        #Eg: if using waitress something like: serve(app, host='0.0.0.0', port=5000, threads=4)

# HTTP versus HTTPS:
#    The code above will try to create SSL certificates with create_ssl_certificate() using OpenSSL. (This will only work if you have OpenSSL installed, and you probably will have to change the path inside the mentioned function). If it fails, you may also generate the certificate in another way to run the server as HTTPS. 
#   Even if you do this, it is no guarantee the browser will accept the self-generated certificate. It might still block the session cookies, which in turn will not allow authentication to happen.
#    
#   If you have the SSL certificate and key file, and cookies are being blocked by the browser when you try to log in: 
#   Get your browser to accept third-party cookies from https://127.0.0.1:5000/ (or whichever port you are runnning this application with)

#   If you do not have the SSL certificate:
#   The app will automatically run HTTP: Get your browser to accept third-party cookies from http://127.0.0.1:5000/ (or whichever port you are runnning this application with). You may have to adjust a couple of things in the Config file according to your browser's feedback. Don't forget to adjust the URL in the React application.