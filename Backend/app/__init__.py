"""
**The app package**

Contains the application files.

--------------------------------------

**create_app(config_class: type[BaseConfig]) --> Flask**: Initializes and configures the Flask application instance from *__init__.py*. The function pulls the extentions from *extensions.py*.

Under app you will also find the directories:
- "models": contains the db models upon which SQLAlchemy will build the database
- "routes": further subdivided per blueprint, contain the apis
- "system_logs": folder that holds the log files
- "utils": where one will find helper functions

"""
# from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import logging
from logging.config import dictConfig
from colorama import init
import app.extensions.extensions as extensions

def create_app(config_class):
    if config_class is None:
        raise ValueError("A configuration class must be provided.")

    # Initialize colorama --> perhaps only needed in development?
    init(autoreset=True) 
    
    # Create application
    app = Flask(__name__)

    # CONFIG Configuration 
    app.config.from_object(config_class)

    # LOGGING Configuration
    if hasattr(config_class, "LOGGING_CONFIG"):
        dictConfig(config_class.LOGGING_CONFIG)# Apply the logging configuration

    system_logger = logging.getLogger("system_log")

    #Attemp to stop file rotation issue:
    from logging.handlers import TimedRotatingFileHandler
    from config.loggig_config import custom_log_namer

    for handler in system_logger.handlers:# Access the handler to set the custom namer
        if isinstance(handler, TimedRotatingFileHandler):
            handler.namer = custom_log_namer  # Set the custom namer for the TimedRotatingFileHandler
            handler.close()
    
    # TODO: a script may still be missing to get rid of old log files

    # Initialization of app extensions
    extensions.cors.init_app(app, supports_credentials=True, resources=r"/api/*", origins=["http://localhost:5173"]) # consider adding allowed origin from requests: https://flask-cors.corydolphin.com/en/latest/api.html#extension TODO: hardcoding the origin is not a good idea --- change this so as to allow for production-specific stuff as well
    extensions.db.init_app(app)
    # extensions.db_migrate(app, extensions.db) ==> TODO: implementation missing
    extensions.flask_bcrypt.init_app(app)
    extensions.limiter.init_app(app)
    extensions.login_manager.init_app(app)
    extensions.mail.init_app(app)
    extensions.server_session.init_app(app)
    from app.extensions import login_manager_config as flask_login_config #imported just to register

    # TODO: eventually substitute the bellow (importing user) when implementing Flask-Migrate like: 
    # from flask_migrate import Migrate 
    # migrate = Migrate()
    # migrate.init_app(app, extensions.db)  # Initialize Flask-Migrate with db
    from app.models import user

    # from flask import current_app

    # Blueprint registration
    # Note admin has nested blueprits: check admin routes file
    from app.routes.auth import auth
    from app.routes.admin.routes import admin
    from app.routes.contact.routes import contact
    from app.routes.user_settings.routes import user_settings
    from app.routes.stats.routes import stats
    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(admin, url_prefix='/api/admin')
    app.register_blueprint(contact, url_prefix='/api/contact')
    app.register_blueprint(stats, url_prefix='/api/stats')
    app.register_blueprint(user_settings, url_prefix='/api/user_settings')

    # TODO remove test route in production
    @app.route('/test/')
    def test_page():
        return '<h1> Testing the App </h1>'
    
    @app.route('/static_debug/') 
    def static_debug():
        return f"Static folder is: {app.static_folder}"

    return app
