# from enum import Enum
import ast
import enum
import logging
from datetime import datetime, timedelta, timezone
from flask_login import UserMixin
from uuid import uuid4
from random import randint
from sqlalchemy import Enum
from utils.print_to_terminal import print_to_terminal
from config.values import SUPER_USER
from app.extensions.extensions import db
from app.utils.constants.account_constants import INPUT_LENGTH
from app.utils.constants.enum_class import SecretKeyPurpose, modelBool
from app.utils.constants.enum_helpers import map_string_to_enum

# TODO: create script to delete entries older than 90 days

def get_uuid():
    return uuid4().hex

def expiration_date():
    """
    Returns a string representation of the date and time 1 hour from now.
    Format: YYYY-MM-DD HH:MM:SS
    """
    expiration_date = datetime.now() + timedelta(hours=1)
    return expiration_date.strftime("%Y-%m-%d %H:%M:%S")

class SecretKey(db.Model, UserMixin):
    """
    SecretKey db model.
    --------------------------------------------------------------
    **Purpose**
    Two-factor authentication actions rely on a secret key. They have a set expiration date/time.  
    
    """
    __tablename__ = "secret_key"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    expiry_date = db.Column(db.DateTime, default=expiration_date, nullable=False)
    was_used = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False)
    uuid = db.Column(db.String(32), unique=True, default=get_uuid, nullable=False)
    purpose = db.Column(db.Enum(SecretKeyPurpose), nullable=False)
    ip_address = db.Column(db.String(250), nullable=True) # ip address of the request
    user_agent = db.Column(db.String(250), nullable=True) # some device information
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, user_id, purpose, ip_address=None, user_agent=None, **kwargs):
        self.user_id = user_id
        self.purpose = purpose
        self.ip_address = ip_address
        self.user_agent = user_agent
    
    def __repr__(self):
        return f"<SecretKey: {self.id} for {self.purpose} created>"
    
    def is_valid(self):
        """
        is_valid()-> bool
        -----------------------------
        Returns a boolean indicated whether the secret key is still valid or not.
        """
        if self.was_used == modelBool.TRUE:
            return False
        date_now = datetime.now(timezone.utc)

        # Check if the current time is within the validity window
        # (after created_at but before or equal to expiry_date)
        if self.created_at < date_now <= self.expiry_date:
            return True

        # Otherwise, it's not valid
        return False
    
    def mark_as_used(self):
        """
        mark_as_used()-> bool
        -----------------------------
        Invalidates secret key.
        """
        self.was_used = modelBool.TRUE