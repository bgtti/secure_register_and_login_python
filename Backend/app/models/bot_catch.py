from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

class BotCatch(UserMixin, db.Model):
    """
    Used to store ip addresses that have been blocked from making requests.
    (used to stop known bots)
    -------------------------------------------------
    Important note:
    Since these are considered bots, IP addresses should not be anonymous and do not need hashing.
    IP addresses should be checked for validity before being stored.
    -------------------------------------------------
    Example usage:

    ...
    
    """
    __tablename__ = "bot_catch"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    ip_address = db.Column(db.String(250), nullable=True)
    country = db.Column(db.String(90), nullable=True)
    user_agent = db.Column(db.String(250), nullable=True)
    form_targeted = db.Column(db.String(100), nullable=True)
    date_accessed = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, ip_address, country, user_agent, **kwargs):
        self.ip_address = ip_address
        self.country = country
        self.user_agent = user_agent
    
    def __repr__(self):
        return f"<IP blocked {self.ip_address}>"