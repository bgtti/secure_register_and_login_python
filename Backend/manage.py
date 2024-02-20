# Application script: where instance is defined
from app import create_app
from create_db import create_super_admin_acct
from app.extensions import db
from app.config import ProductionConfig

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

if __name__ == "__main__":
    if MODE == "dev":
        app.run(debug=True)
    else:
        app.run() # set accordingly for production. 
        #Eg: if using waitress something like: serve(app, host='0.0.0.0', port=5000, threads=4)

