# Application script: where instance is defined
from app import create_app
from create_db import create_admin_acct
from app.extensions import db
from app.config import ProductionConfig

# Environment can be changed by setting mode to 'dev' during development and 'prod' (for instance) for production
# The app's configuration is found in app/config.py, and pulled by the create_app application factory in app/__init__.py which will use the Config class to configure by default. When mode = 'prod' (or something other than 'dev'), it will create the app using the ProductionConfig class.
# More information on how to handle configuration is available in the flask docs: https://flask.palletsprojects.com/en/3.0.x/config/

# note about ip-address and related functions: remote_addr will be 127.0.0.1 in dev mode, which means the ip-geolocation will be useless (in the stats module). 

mode = "dev" # "prod"

if mode == "dev":
    app = create_app()
else:
    app = create_app(ProductionConfig)

with app.app_context():
    db.create_all()
    create_admin_acct()

if __name__ == '__main__':
    if mode == 'dev':
        app.run(debug=True)
    else:
        app.run() # set accordingly for production. 
        #Eg: if using waitress something like: serve(app, host='0.0.0.0', port=5000, threads=4)

