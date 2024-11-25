# from enum import Enum
import ast
import enum
import logging
from datetime import datetime, timedelta, timezone
from flask_login import UserMixin
from uuid import uuid4
import secrets
from random import randint
from sqlalchemy import Enum
from utils.print_to_terminal import print_to_terminal
from config.values import SUPER_USER
from app.extensions.extensions import db
from app.utils.constants.account_constants import INPUT_LENGTH
from app.utils.constants.enum_class import modelBool
from app.utils.constants.enum_helpers import map_string_to_enum

# TODO: create script to delete entries older than 90 days

# What is SecretKey supposed to do: check https://stackoverflow.com/questions/23039734/flask-login-password-reset

def get_token():
    return secrets.token_urlsafe(32)

def expiration_date():
    """
    Returns a string representation of the date and time 1 hour from now.
    Format: YYYY-MM-DD HH:MM:SS
    """
    expiration_date = datetime.now() + timedelta(hours=1)
    return expiration_date.strftime("%Y-%m-%d %H:%M:%S")

# class TokenPurpose(enum.Enum):
#     """
#     `TokenPurpose` is an Enum to indicate the purpose for which a Token was created.
#     Currently secret keys are used to validate a request to change password or email.

#     ------------------------------------------------------------
#     **Options:**
    
#     - `EMAIL_CHANGE = "email_change"` 
#     - `PASSWORD_CHANGE = "password_change"`
#     - `AUTH_FACTOR = "auth_factor"` 
#     - `VERIFY_EMAIL = "verify_email"`
#     """
#     VERIFY_EMAIL = "verify_email" 
#     EMAIL_CHANGE = "verify_new_email" 
#     PASSWORD_CHANGE = "password_change" 

class ValidationToken(db.Model, UserMixin):
    """
    Token db model.
    --------------------------------------------------------------
    **Purpose**
    Two-factor authentication actions rely on a secret key. They have a set expiration date/time.  
    
    """
    __tablename__ = "validation_token"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    token = db.Column(db.String(32), unique=True, default=get_token, nullable=False)
    token_verified = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False) # user used the token
    # email change requests will require a second token
    new_email_token = db.Column(db.String(32), unique=True, default=get_token, nullable=False)
    new_email_token_verified = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False) # user used the token
    # token creation info
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    expiry_date = db.Column(db.DateTime, default=expiration_date, nullable=False)
    ip_address = db.Column(db.String(250), nullable=True) # ip address of the request
    user_agent = db.Column(db.String(250), nullable=True) # some device information
    # token belonging info
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, user_id, ip_address=None, user_agent=None, **kwargs):
        self.user_id = user_id
        self.ip_address = ip_address
        self.user_agent = user_agent
    
    def __repr__(self):
        return f"<Token: {self.id} created>"
    
    def validate_token(self):
        """
        validate_token()-> bool
        -----------------------------
        Will return true if the token is valid and false otherwise.
        Will mark the token as used by setting token_verified to true.
        """
        now = datetime.now(timezone.utc)
        token_is_valid = self.created_at < now <= self.expiry_date
        token_was_not_used = self.token_verified == modelBool.FALSE

        if token_is_valid and token_was_not_used:
            self.token_verified = modelBool.TRUE
            return True
        else:
            return False
    
    def validate_email_token(self):
        """
        validate_email_token()-> bool
        -----------------------------
        Will return true if the new_email_token is valid and false otherwise.
        Will mark the new_email_token as used by setting new_email_token_verified to true.
        """
        now = datetime.now(timezone.utc)
        token_is_valid = self.created_at < now <= self.expiry_date
        token_was_not_used = self.new_email_token_verified == modelBool.FALSE

        if token_is_valid and token_was_not_used:
            self.new_email_token_verified = modelBool.TRUE
            return True
        else:
            return False
    
    def user_may_change_email(self):
        """
        user_may_change_email()-> bool
        -----------------------------
        Will return true if both tokens were verified and they are still valid.
        Will return false otherwise.
        """
        now = datetime.now(timezone.utc)
        token_is_valid = self.created_at < now <= self.expiry_date
        old_email_verified = self.token_verified == modelBool.TRUE
        new_email_verified = self.token_verified == modelBool.TRUE

        if token_is_valid and old_email_verified and new_email_verified:
            return True
        else:
            return False





# TODO RUN PERIODICALLY with celery, apsscheduler, or a cron job:
# from flask import current_app

# def cleanup_expired_tokens():
#     with current_app.app_context():
#         expired_tokens = ValidationToken.query.filter(ValidationToken.expires_at < datetime.utcnow()).all()
#         for token in expired_tokens:
#             db.session.delete(token)
#         db.session.commit()