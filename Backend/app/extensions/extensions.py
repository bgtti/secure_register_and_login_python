"""
**ABOUT THIS FILE**

extensions.py centralizes the initialization of reusable Flask extensions and application-wide utilities. 

--------------------
**What this file does**

This file allows for clean separation of concerns by:
- Declaring and configuring extensions in a single place.
- Enabling lazy initialization with the application (via the Flask app factory pattern).
- Promoting consistency, maintainability, and scalability in the application structure.

In short, extensions.py provides a unified way to manage third-party integrations and shared components in this Flask app.

--------------------
**How this file is used**

Some extensions listed here that are required for the app's configuration are imported into and initialized in the app/__init__ file, where the app is created (*create_app* function).
Files throughout the application make use of the extensions here. 

--------------------
**Example**

The database Object Relational Mapper SQLAlchemy, for instance, is declared here as `db = SQLAlchemy()`, and could be imported into other files like so: `from app.extensions.extensions import db`

"""
from cryptography.fernet import Fernet
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from itsdangerous import URLSafeTimedSerializer
from sqids import Sqids
from config.values import SERIALIZER_SECRET_KEY, ENCRYPTION_KEY

db = SQLAlchemy()
"""`db` refers to the extension `SQLAlchemy`, a toolkit and ORM that allows devs to access and manage SQL databases."""

# db_migrate = Migrate() ==> TODO: implementation missing
"""`db_migrate` refers to the extension `Flask-Migrate`, which handles SQLAlchemy database migrations for Flask applications using Alembic."""

cipher = Fernet(ENCRYPTION_KEY)
"""`cipher` refers to the extension `cryptography`, where `Fernet` (symmetric encryption) is used to encrypt strings."""

cors = CORS()
"""`cors` refers to the extension `Flask-CORS`, which handles Cross-Origin Resource Sharing (CORS) to allow or restrict resource sharing between different domains."""

faker = Faker()
"""`faker` is an instance of `Faker`, a library used to generate fake data for testing and seeding databases."""

flask_bcrypt = Bcrypt()
"""`flask_bcrypt` is an instance of `Flask-Bcrypt`, which provides bcrypt hashing utilities for securely storing passwords."""

limiter = Limiter(key_func=get_remote_address)
"""`limiter` refers to the extension `Flask-Limiter`, which is used to apply rate-limiting to Flask routes. 
It uses `get_remote_address` to determine the source of requests."""

login_manager = LoginManager()
"""`login_manager` refers to the extension `Flask-Login`, which manages user sessions, including login/logout functionality."""

mail = Mail()
"""`mail` is an instance of `Flask-Mail`, used to send emails through the Flask application."""

serializer = URLSafeTimedSerializer(SERIALIZER_SECRET_KEY) 
"""`serializer` refers to `itsdangerous.URLSafeTimedSerializer`, which is used to sign, timestamp, and validate tokens or data securely."""

server_session = Session() 
"""`server_session` refers to the extension `Flask-Session`, a *session middleware* which enables server-side session management. 
Without it, Flask defaults to client-side cookies for sessions."""

# I may not be using sqids: check and consider removing from requirements
sqids = Sqids(min_length=8)
"""`sqids` is an instance of `Sqids`, a library for generating unique, human-friendly, and customizable IDs."""





