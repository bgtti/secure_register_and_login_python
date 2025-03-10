"""
**ABOUT THIS FILE**

models/log_activity.py contains:

- Constants required for the db model or methods to function
- Helper functions used only in the db model or methods 
- **LogActivity** class (the db model)

--------------

**About Logs**

There are two separate logs used by this app
    1. Log activity (this db model): logs user actions to the db. When linked to a subscribed user, messages logged are also displayed to the user. Used to log activity such as login and password changes. Users with admin roles have access to user logs as well.
    2. System logs: logs all system events to a file which may be used by developers for debugging purposes. System logs are configured in the app's config file and saved in files inside the folder system_logs.

**Beware of log content**

Developers must take care of the contents being logged. Do not log plaintext passwords or sensitive information.

"""
# Python/Flask libraries
from sqlalchemy.ext.hybrid import hybrid_property #DELETE
from datetime import datetime, timezone #DELETE
# Extensions and configurations
from flask_login import UserMixin
from app.extensions.extensions import db
from app.extensions.sqlalchemy_config import EncryptedType, UTCDateTime

from app.utils.ip_utils.ip_geolocation import geolocate_ip
from app.utils.ip_utils.ip_anonymization import anonymize_ip

# NOTE (idea): create function to delete old logs on a schedule

LOG_LEVEL = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "SUSPICIOUS":25,
    "INFO": 20,
    "BOT":15, # for bots caught in honeypot
    "DEBUG": 10,
    "NOTSET": 0
}

def get_log_level(level_name: str) -> dict:
    """
    Parameter: key in LOG_LEVEL dictionary.

    Returns an dictionary with the level name and level id.
    If key is invalid, will default to "NOTSET".
    
    **Example**
    ```
    level = get_log_level("WARNING")
    level -> {
            "level":"WARNING",
            "level_id": 30
            }

    level = get_log_level("hello")
    level -> {
            "level":"NOTSET",
            "level_id": 0
            }
    ```
    """
    name_upper = level_name.upper()
    res = {
        "level": name_upper if name_upper in LOG_LEVEL else "NOTSET",
        "level_id": LOG_LEVEL.get(name_upper, LOG_LEVEL["NOTSET"])
    }
    return res


def get_ip_info(ip: str = "") -> dict:
    """
    Parameter: ip address
    Returns: an dictionary with the anonymized_ip and geo_location

    **Example**
    ```
    ip_info = get_ip_info("192.168.1.1")
    ip_info -> {
            "anonymized_ip":"192.168.1.0",
            "geo_location":"Tokyo, Japan"
            }

    ip_info = get_ip_info()
    ip_info -> {
            "anonymized_ip":"N/A",
            "geo_location":"N/A"
            }
    ```
    """
    res = {
        "anonymized_ip":"N/A",
        "geo_location":"N/A"
    }
    if ip == "":
        return res
    location = geolocate_ip(ip)
    res["geo_location"] = f"{location['city']}, {location['country']}"
    anonymous_ip = anonymize_ip(ip)
    if anonymous_ip is not None:
        res["anonymized_ip"] = anonymous_ip
    return res


class LogActivity(UserMixin, db.Model):
    """
    Use LogActivity to log user activity that would be relevant for debugging a problem the user might have encountered.

    ----------------------------------------------------

    ...

    ----------------------------------------------------

    Example usage for adding to this db:
    ...
    """
    __tablename__ = "log_activity"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    created_at = db.Column(UTCDateTime, default=datetime.now(timezone.utc), index=True)
    level = db.Column(db.String(50), nullable=False)
    level_id = db.Column(db.Integer, nullable=False, index=True)
    activity = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(200), nullable=False) # can be shared with user
    more_info = db.Column(db.String(200), nullable=False) # more details about the log, not to be shared with end user
    anonymized_ip = db.Column(EncryptedType, nullable=True)
    geo_location = db.Column(EncryptedType, nullable=True)
    user_agent = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, nullable=False, index=True, default=0) # if user_id is unknown, default to 0
    
    def __init__(self, level, activity, message, more_info, ip, user_agent, user_id=0):
        level_info = get_log_level(level)
        self.level = level_info["level"]
        self.level_id = level_info["level_id"]
        self.activity = activity
        self.message = message
        self.more_info = more_info
        ip_info = get_ip_info(ip)
        self.geo_location = ip_info["geo_location"]
        self.anonymized_ip = ip_info["anonymized_ip"]
        self.user_agent = user_agent
        self.user_id = user_id
    
    def __repr__(self):
        return f"<Log: {self.id} {self.level} {self.message}>"
    
    def serialize_user_logs(self):
        return {
            "user_id": self.user_id,
            "created_at": self.created_at,
            "level": self.level,
            "activity": self.activity,
            "message": self.message,
        }