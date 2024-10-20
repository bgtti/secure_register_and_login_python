# Application script: where instance is defined
from app import create_app
from create_db import create_super_admin_acct, check_redis, create_ssl_certificate
from app.extensions import db 
from app.config import ProductionConfig
import os

# ABOUT MODE:
# Environment can be changed by setting MODE to 'dev' during development and 'prod' (for instance) for production
# The app's configuration is found in app/config.py, and pulled by the create_app application factory in app/__init__.py which will use the Config class to configure by default. When MODE = 'prod' (or something other than 'dev'), it will create the app using the ProductionConfig class.
# More information on how to handle configuration is available in the flask docs: https://flask.palletsprojects.com/en/3.0.x/config/
# note about ip-address and related functions: remote_addr will be 127.0.0.1 in dev MODE, which means the ip-geolocation will be useless (in the stats module). 

MODE = "dev" # "prod"

if MODE == "dev":
    app = create_app()
else:
    SHOW_WARNINGS = False
    app = create_app(ProductionConfig)

with app.app_context():
    db.create_all()
    create_super_admin_acct()
    if MODE == "dev":
        from app.dummie_data.dummie_users import create_dummie_user_accts
        create_dummie_user_accts()
        check_redis()
        create_ssl_certificate()

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
    if MODE == "dev":
        from app.utils.console_warning.print_warning import console_warn
        # If an SSL certificate and key are available in the specified folder, they will be used to build an HTTP connection. This is recommended.
        if os.path.exists(os.path.join(os.getcwd(), "ssl_certificate")) and os.listdir(os.path.join(os.getcwd(), "ssl_certificate")):
            console_warn(f"App running in HTTPS: be sure to check front end path.", "BLUE")
            app.run(ssl_context=("ssl_certificate/cert.pem", "ssl_certificate/key.pem"), debug=True)
        else:
            console_warn(f"App running in HTTP: be sure to check front end path.", "BLUE")
            app.run(debug=True)
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