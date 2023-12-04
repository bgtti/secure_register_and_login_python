from flask import Flask
from app.config import Config
import app.extensions as extensions
from flask_sqlalchemy import SQLAlchemy
import os

# consider: login manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    extensions.db.init_app(app)
    extensions.flask_bcrypt.init_app(app)
    extensions.jwt.init_app(app)
    extensions.cors.init_app(app)

    from app.models import user
    from flask import current_app

    from app.account.routes import account
    from app.admin.routes import admin
    app.register_blueprint(account, url_prefix='/api/account')
    app.register_blueprint(admin, url_prefix='/api/admin')

    @app.route('/test/')
    def test_page():
        return '<h1> Testing the App </h1>'

    # ABS_PATH = os.path.dirname(__file__)
    # REL_PATH = "static"
    # STATIC_PATH = repr(str(app.config["STATIC_FOLDER"]))

    # @app.route("/../static/<filename>")
    # def static_path():
    #     pass

    return app
