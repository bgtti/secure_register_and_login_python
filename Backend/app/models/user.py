from flask_login import UserMixin
import ast
from datetime import datetime, timedelta
from uuid import uuid4
from app.extensions import db
from app.config import ADMIN_ACCT
from app.utils.constants.account_constants import INPUT_LENGTH

ADMIN_DATA = ast.literal_eval(ADMIN_ACCT)
ADMIN_PW = ADMIN_DATA[2]

# uuid generation
def get_uuid():
    return uuid4().hex

# Notes:
# - Bcrypt should output a 60-character string, so this was used as maximum password length
# - User blockage: the user can be blocked from accessing the account by an admin by setting _is_blocked to true.
# - The user can also be temporarily blocked for failing to log in too many times, where _login_blocked will be set to true. 
# - access_level should be either "user" or "admin". Change access_level using make_user_admin

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    _uuid = db.Column(db.String(32), unique=True, default=get_uuid)
    _name = db.Column(db.String(INPUT_LENGTH['name']['maxValue']), nullable=False)
    _email = db.Column(db.String(INPUT_LENGTH['email']['maxValue']), nullable=False, unique=True)
    _password = db.Column(db.String(60), nullable=False)
    _salt = db.Column(db.String(8), nullable=False)
    _created_at = db.Column(db.DateTime, default=datetime.utcnow)
    _session = db.Column(db.String(32), nullable=True, default="")
    _last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    _access_level = db.Column(db.String(5), default="user", nullable=False)
    _is_blocked = db.Column(db.String(5), default="false", nullable=False)
    _login_attempts = db.Column(db.Integer, default=0)
    _last_login_attempt = db.Column(db.DateTime, default=datetime.utcnow)
    _login_blocked = db.Column(db.String(5), default="false", nullable=False)
    _login_blocked_until = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    def __init__(self, name, email, password, salt, created_at, **kwargs):
        self._name = name
        self._email = email
        self._password = password
        self._salt = salt
        self._created_at = created_at
    
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
    def session(self):
        return self._session
    
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
    
    def new_session(self):
        new_session_id = get_uuid()
        self._session = new_session_id
        return self._session 
    
    def end_session(self):
        self._session = ""
    
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

    def make_user_admin(self, admin_password):
        """
        Default admin password required
        """
        if admin_password == ADMIN_PW:
            self._access_level = "admin" 
    
    def serialize_user_table(self):
        return {
            "uuid": self._uuid,
            "name": self._name,
            "email": self._email,
            "last_seen": self._last_seen,
            "is_blocked": self._is_blocked,
        }