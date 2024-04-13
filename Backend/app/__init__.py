from flask import Flask
from app.config import Config, TestConfig, LOGGING_CONFIG
import app.extensions as extensions
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.config import dictConfig
from colorama import init

def create_app(config_class=Config):
    init(autoreset=True)  # Initialize colorama
    
    app = Flask(__name__)
    app.config.from_object(config_class)

    dictConfig(LOGGING_CONFIG)
    system_logger = logging.getLogger("system_log")

    extensions.flask_bcrypt.init_app(app)
    extensions.cors.init_app(app, supports_credentials=True, resources=r"/api/*", origins=["http://localhost:5173"]) # consider adding allowed origin from requests: https://flask-cors.corydolphin.com/en/latest/api.html#extension
    extensions.login_manager.init_app(app)
    # extensions.server_session.init_app(app)
    extensions.db.init_app(app)
    extensions.limiter.init_app(app)
    extensions.mail.init_app(app)

    from app.models import user
    from flask import current_app

    # Registering blueprints
    # Note admin has nested blueprits: check admin routes file
    from app.routes.account.routes import account
    from app.routes.admin.routes import admin
    from app.routes.stats.routes import stats
    from app.routes.contact.routes import contact
    app.register_blueprint(account, url_prefix='/api/account')
    app.register_blueprint(admin, url_prefix='/api/admin')
    app.register_blueprint(stats, url_prefix='/api/stats')
    app.register_blueprint(contact, url_prefix='/api/contact')

    @app.route('/test/')
    def test_page():
        return '<h1> Testing the App </h1>'

    return app
