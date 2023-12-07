from app.extensions import db
from sqlalchemy import event
from flask_login import UserMixin
from datetime import datetime
from uuid import uuid4
from app.account.constants import INPUT_LENGTH 

# IN THIS FILE: User DB Model

# uuid generation
def get_uuid():
    return uuid4().hex

# Bcrypt should output a 60-character string, so this was used as maximum password length

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    _uuid = db.Column(db.String(32), unique=True, default=get_uuid)
    _name = db.Column(db.String(INPUT_LENGTH['name']['maxValue']), nullable=False)
    _email = db.Column(db.String(INPUT_LENGTH['email']['maxValue']), nullable=False, unique=True)
    _password = db.Column(db.String(60), nullable=False)
    _salt = db.Column(db.String(8), nullable=False)
    _created_at = db.Column(db.DateTime, default=datetime.utcnow)
    _access_level = db.Column(db.String(5), default="user")
    
    
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