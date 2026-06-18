"""
`models/log_security.py` contains:

**LogSecurity** class (the db model)

Security logs contain events related to security and are used to track safety-relevant events in the system.
These are used to detect threats and investigate compliance issues.

Examples:
Authentication events, admin activity, or similar.
See full list in `app/constants/log_events_security.py`

Retention period:
It is recommended that security logs are kept for a period of 1-2 years.

Log deletion:
Security logs should never be deleted or modified.
Developers should not create endpoints that allow for security logs editting.
Only a DB retention script (cron job, CLI command) should delete old rows.

--------------

**About Logs**

There are two separate logs used by this app
    1. Log activity and security: logs user actions to the db. 
    2. System logs: logs all system events to a file which may be used by developers for debugging purposes. System logs are configured in the app's config file and saved in files inside the folder system_logs.

**Beware of log content**

Developers must take care of the contents being logged. Do not log plaintext passwords or sensitive information.

"""
# Python/Flask libraries
from datetime import datetime, timezone 

# Extensions and configurations
from sqlalchemy import event
from sqlalchemy.orm import mapper
from flask_login import UserMixin
from app.extensions.extensions import db
from app.extensions.sqlalchemy_config import EncryptedType, UTCDateTime

# Constants and helpers
from app.constants.log_events_security import SecurityEvent
from app.common.log_utils.get_log_level import get_log_level
from app.common.ip_utils.ip_geolocation import geolocate_ip
from app.common.ip_utils.ip_anonymization import anonymize_ip

# TODO (idea): create function to delete old logs on a schedule

class LogSecurity(UserMixin, db.Model):
    """
    Use LogSecurity to log all security-relevant events (such as login attempts,
    suspicious activity, admin actions, rate limiting, etc.). 

    A full list of events is available in `app/logging/events_security.py`

    **Do not allow deletion or modification by users or admins.**

    ----------------------------------------------------
    Fields overview:

    :param created_at:   When the event was logged.
    :param level:        Human-readable log level (e.g. "INFO", "WARNING", "ERROR").
    :param level_id:     Numeric log level (see constant LOG_LEVEL dict).
    :param event:        SecurityEvent enum value (see `app/logging/events_security.py`).
    :param message:      Short description of the event. Safe to show to end users.
    :param more_info:    Internal technical details for developers / admins only.
    :param resource_type/resource_id:
                    *Optional*: what object this event refers to, e.g.
                    resource_type="User",  resource_id=<user_id>
                    resource_type="Message", resource_id=<message_id>
    :param anonymized_ip:  IP address in anonymized form (for long-term stats).
    :param ip_address:     Full IP address (PII – used short term only).
    :param geo_location:   Geolocation derived from IP (country/city).
    :param user_agent:     HTTP User-Agent string.
    :param user_id:        ID of the user who triggered the event (or 0 if unknown).

    ----------------------------------------------------
    Creating a new log:

    Example usage for adding to this db:
    ```
    log = LogSecurity(
        level="INFO",
        event=SecurityEvent.LOGIN_SUCCESS,
        message="User logged in successfully.",
        more_info="Login via password on /login endpoint.",
        ip=request.remote_addr,
        user_agent=request.user_agent.string,
        user_id=current_user.id if current_user.is_authenticated else 0,
        )
    db.session.add(log)
    db.session.commit()
    ```
    """
    __tablename__ = "log_security"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    # created_at = db.Column(UTCDateTime, default=datetime.now(timezone.utc), index=True)
    created_at = db.Column(UTCDateTime, default=lambda: datetime.now(timezone.utc), index=True, nullable=False)

    # Log level: anything above "info" should trigger alert or flag
    level = db.Column(db.String(50), nullable=False)
    level_id = db.Column(db.Integer, nullable=False, index=True)

    # Event topic: see SecurityEvent Enum
    event = db.Column(db.Enum(SecurityEvent), nullable=False)

    # Activity: the action the caller function was trying to perform. Ex.: change password
    activity = db.Column(db.String(200), nullable=False)

    # Log text/description/message
    message = db.Column(db.String(200), nullable=False) # ps: log messages can be shared with user
    more_info = db.Column(db.String(200), nullable=False) # more details about the log - intended for devs, not to be shared with users

    # Information about the resource targeted by the event (if any)
    resource_type = db.Column(db.String(50), nullable=True) # Example: "Message", "User" TODO: NOT BEING USED
    resource_id = db.Column(db.Integer, nullable=True) # If a resource was changed (example: user deleted), include the user id here. If a message was sent, include message id. TODO: NOT BEING USED

    # Anonymized information
    anonymized_ip = db.Column(EncryptedType, nullable=True)

    # User-identifiable information
    ip_address = db.Column(EncryptedType, nullable=True)
    geo_location = db.Column(EncryptedType, nullable=True)
    user_agent = db.Column(db.String(250), nullable=True)

    # User
    user_id = db.Column(db.Integer, nullable=False, index=True, default=0) # if user_id is unknown, default to 0
    
    def __init__(self, level, event, activity, message, more_info, ip, user_agent, user_id=0, **kwargs):
        """
        Constructor runs automatically when a new log is created.

        Requires: 
        - level: a log-level member of constant LOG_LEVEL dictionary
        - event: SecurityEvent enum
        - message: description of the event (shall be available to user)
        - more_info: detailed description of the event
        - ip: ip address of the user
        - user_agent: HTTP User-Agent request header
        - user_id: the user's id or, if user is unkown, 0
        """
        level_info = get_log_level(level)
        self.level = level_info["level"]
        self.level_id = level_info["level_id"]
        self.event = event
        self.activity = activity
        self.message = message
        self.more_info = more_info
        self.ip_address = ip
        location = geolocate_ip(ip)
        self.geo_location = f"{location['city']}, {location['country']}"
        self.anonymized_ip = anonymize_ip(ip)
        self.user_agent = user_agent
        self.user_id = user_id
    
    def __repr__(self):
        """How message is logged in the dev's console"""
        return f"<Security log: {self.id} {self.level} {self.message}>"
    
    def serialize_security_logs(self):
        """Serializes logs for the client"""
        return {
            "created_at": self.created_at,
            "level": self.level,
            "event": self.event.value,
            "message": self.message,
        }
    
    def anonymize(self):
        """Anonymize if user deletes account"""
        self.ip_address = None
        self.geo_location = None
        self.user_agent = None
    
@event.listens_for(LogSecurity, "before_update")
def prevent_log_update(mapper, connection, target):
    raise RuntimeError("SECURITY LOG IMMUTABILITY VIOLATION: update attempted")

@event.listens_for(LogSecurity, "before_delete")
def prevent_log_delete(mapper, connection, target):
    raise RuntimeError("SECURITY LOG IMMUTABILITY VIOLATION: delete attempted")


# use this in user deletion logic:
# def anonymize_logs_for_user(user_id: int):
#     logs = LogSecurity.query.filter_by(user_id=user_id).all()
#     for log in logs:
#         log.anonymize()
#     db.session.commit()  

# OOOR bulk anonymize -- might need this to bypass event listener:
# from app.extensions import db
# from app.models.log_event import LogSecurity

# def anonymize_logs_for_user(user_id: int):
#     (
#         LogSecurity.query
#         .filter_by(user_id=user_id)
#         .update(
#             {
#                 LogSecurity.ip_address: None,
#                 LogSecurity.geo_location: None,
#                 LogSecurity.user_agent: None,
#             },
#             synchronize_session=False,
#         )
#     )
#     db.session.commit()