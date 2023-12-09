from app.extensions import db
from sqlalchemy import event
from flask_login import UserMixin
from datetime import datetime, timedelta
from uuid import uuid4
from app.account.constants import INPUT_LENGTH 

# IN THIS FILE: User DB Model

# uuid generation
def get_uuid():
    return uuid4().hex

# Notes:
# - Bcrypt should output a 60-character string, so this was used as maximum password length
# - User blockage: the user can be blocked from accessing the account by an admin by setting _is_blocked to true.
# - The user can also be temporarily blocked for failing to log in too many times, where _login_blocked will be set to true. 

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    _uuid = db.Column(db.String(32), unique=True, default=get_uuid)
    _name = db.Column(db.String(INPUT_LENGTH['name']['maxValue']), nullable=False)
    _email = db.Column(db.String(INPUT_LENGTH['email']['maxValue']), nullable=False, unique=True)
    _password = db.Column(db.String(60), nullable=False)
    _salt = db.Column(db.String(8), nullable=False)
    _created_at = db.Column(db.DateTime, default=datetime.utcnow)
    _last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    _access_level = db.Column(db.String(5), default="user", nullable=False)
    _is_blocked = db.Column(db.String(5), default="false", nullable=False)
    _login_attempts = db.Column(db.Integer, default=0)
    _last_login_attempt = db.Column(db.DateTime, default=datetime.utcnow)
    _login_blocked = db.Column(db.String(5), default="false", nullable=False)
    _login_blocked_until = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    def __init__(self, email, name, password, salt,**kwargs):
        self._email = email
        self._name = name
        self._password = password
        self._salt = salt
        self._created_at = datetime.utcnow()
    
    def __repr__(self):
        return f"<User: {self.id} {self._name} {self._email}>"
    
    @property
    def uuid(self):
        return self._uuid

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email
    
    @property
    def password(self):
        return self._password
    
    @property
    def salt(self):
        return self._salt
    
    @property
    def access_level(self):
        return self._access_level
    
    @property
    def created_at(self):
        return self._created_at
    
    @property
    def last_seen(self):
        return self._last_seen
    
    @property
    def is_blocked(self):
        return self._is_blocked

    @property
    def login_attempts(self):
        return self._login_attempts

    @property
    def last_login_attempt(self):
        return self._last_login_attempt
    
    @property
    def login_blocked(self):
        return self._login_blocked

    @property
    def login_blocked_until(self):
        return self._login_blocked_until
    
    def increment_login_attempts(self):
        self._login_attempts += 1
        self._last_login_attempt = datetime.utcnow()
        if self._login_attempts == 3:
            self._login_blocked = "true"
            self._login_blocked_until = datetime.utcnow() + timedelta(minutes=1)
        elif self._login_attempts == 5:
            self._login_blocked_until = datetime.utcnow() +timedelta(minutes=2)
        elif self._login_attempts > 5:
            self._login_blocked_until = datetime.utcnow() + timedelta(minutes=5)

    def reset_login_attempts(self):
        self._login_attempts = 0
        self._last_login_attempt = datetime.utcnow()
        self._login_blocked_until = datetime.utcnow()
        self._login_blocked = "false"

    def is_login_blocked(self):
        return self._login_blocked == "true" and self._login_blocked_until > datetime.utcnow()
    
    def has_access_blocked(self):
        return self._is_blocked == "true" 
    
    def block_access(self):
        self._is_blocked = "true" 
    
    def unblock_access(self):
        self._is_blocked = "false" 