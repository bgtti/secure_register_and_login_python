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

# TODO: implement in user model. Currently not implemented or used anywhere

class Roles(db.Model, UserMixin):
    """
    Role db model.
    --------------------------------------------------------------
    **Purpose**
    define user role-based access.  
    
    """
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    role = db.Column(db.String(32), unique=True, nullable=False)
    
    def __init__(self, user_id, ip_address=None, user_agent=None, **kwargs):
        self.user_id = user_id
        self.ip_address = ip_address
        self.user_agent = user_agent
    
    def __repr__(self):
        return f"<Token: {self.id} created>"