"""
`models/bot_trap.py` contains:

**BotTrap** class (the db model) which stores infomation about bots trapped in form Honeypots.
"""
# Python/Flask libraries
from datetime import datetime, timezone 

# Extensions and configurations
from flask_login import UserMixin
from app.extensions.extensions import db
from app.extensions.sqlalchemy_config import EncryptedType, UTCDateTime

# Constants and helpers
from app.common.ip_utils.ip_geolocation import geolocate_ip


class BotTrap(UserMixin, db.Model):
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
    __tablename__ = "bot_trap"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    # created_at = db.Column(UTCDateTime, default=datetime.now(timezone.utc), index=True)
    created_at = db.Column(UTCDateTime, default=lambda: datetime.now(timezone.utc), index=True, nullable=False)
    # Target
    form_targeted = db.Column(db.String(100), nullable=True)
    endpoint = db.Column(db.String(100), nullable=True) #eh: /api/signup, etc
    # Source/fingerprinting
    ip_address = db.Column(EncryptedType, nullable=True)
    geo_location = db.Column(EncryptedType, nullable=True)
    user_agent = db.Column(db.String(250), nullable=True)
    referrer = db.Column(db.String(100), nullable=True) # referrer origin

    def __init__(self, form_targeted, endpoint, ip, geo_location, user_agent, referrer, **kwargs):
        self.form_targeted = form_targeted
        self.endpoint = endpoint
        self.ip_address = ip
        self.geo_location = geo_location # String like: city, country 
        self.user_agent = user_agent
        self.referrer = referrer
    
    def __repr__(self):
        return f"<Bot caught using ip: {self.ip_address}>"