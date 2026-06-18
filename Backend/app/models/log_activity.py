"""
**ABOUT THIS FILE**

models/log_activity.py contains:

**LogActivity** class (the db model)

Activity logs contain events that might be relevant to debug a user issue.

Examples:
Non-security relevant events such as changes in profile.
See full list in `app/constants/log_events_action.py`

Retention period:
It is recommended that activity logs are kept for a period of 3-6 months.

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
from flask_login import UserMixin
from app.extensions.extensions import db
from app.extensions.sqlalchemy_config import EncryptedType, UTCDateTime

# Constants and helpers
from app.constants.log_events_action import ActionEvent
from app.common.log_utils.get_log_level import get_log_level
from app.common.ip_utils.ip_geolocation import geolocate_ip
from app.common.ip_utils.ip_anonymization import anonymize_ip

# TODO (idea): create function to delete old logs on a schedule


class LogActivity(UserMixin, db.Model):
    """
    Use LogActivity to log user activity that would be relevant for debugging a problem the user might have encountered.
    
    A full list of events is available in `app/logging/events_activity.py`

    ----------------------------------------------------
    Fields overview:

    - created_at:   When the event was logged.
    - level:        Human-readable log level (e.g. "INFO", "WARNING", "ERROR").
    - level_id:     Numeric log level (see constant LOG_LEVEL dict).
    - event:        ActionEvent enum value (see `app/logging/events_security.py`).
    - message:      Short description of the event. Safe to show to end users.
    - more_info:    Internal technical details for developers / admins only.
    - resource_type/resource_id:
                    *Optional*: what object this event refers to, e.g.
                    resource_type="User",  resource_id=<user_id>
                    resource_type="Message", resource_id=<message_id>
    - anonymized_ip:  IP address in anonymized form (for long-term stats).
    - ip_address:     Full IP address (PII – used short term only).
    - geo_location:   Geolocation derived from IP (country/city).
    - user_agent:     HTTP User-Agent string.
    - user_id:        ID of the user who triggered the event (or 0 if unknown).

    ----------------------------------------------------
    Creating a new log:

    Example usage for adding to this db:
    ```
    log = LogSecurity(
        level="INFO",
        event=ActionEvent.USER_PROFILE_UPDATED,
        message="User updated profile successfully.",
        more_info="User changed profile name.",
        ip=request.remote_addr,
        user_agent=request.user_agent.string,
        user_id=current_user.id if current_user.is_authenticated else 0,
        )
    db.session.add(log)
    db.session.commit()
    ```
    """
    __tablename__ = "log_activity"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    # created_at = db.Column(UTCDateTime, default=datetime.now(timezone.utc), index=True)
    created_at = db.Column(UTCDateTime, default=lambda: datetime.now(timezone.utc), index=True, nullable=False)

    # Log level: anything above "info" should trigger alert or flag
    level = db.Column(db.String(50), nullable=False)
    level_id = db.Column(db.Integer, nullable=False, index=True)

    # Event topic: see ActionEvent Enum
    event = db.Column(db.Enum(ActionEvent), nullable=False)

    # Activity: the action the caller function was trying to perform. Ex.: change user preferences
    activity = db.Column(db.String(200), nullable=False)

    # Log text/description/message
    message = db.Column(db.String(200), nullable=False) # ps: log messages can be shared with user
    more_info = db.Column(db.String(200), nullable=False) # more details about the log - intended for devs, not to be shared with users

    # Information about the resource targeted by the event (if any)
    resource_type = db.Column(db.String(50), nullable=True) # Example: "Message", "User"
    resource_id = db.Column(db.Integer, nullable=True) # If a resource was changed (example: user deleted), include the user id here. If a message was sent, include message id.

    # Anonymized information
    anonymized_ip = db.Column(EncryptedType, nullable=True)

    # User-identifiable information
    # ip_address = db.Column(EncryptedType, nullable=True)
    # geo_location = db.Column(EncryptedType, nullable=True) #unnecessary... too much info
    user_agent = db.Column(db.String(250), nullable=True)

    # User
    user_id = db.Column(db.Integer, nullable=False, index=True, default=0) # if user_id is unknown, default to 0
    
    def __init__(self, level, event, activity, message, more_info, ip, user_agent, user_id=0, **kwargs):
        """
        Constructor runs automatically when a new log is created.

        Requires: 
        - level: a log-level member of LOG_LEVEL dictionary in constants
        - event: ActionEvent enum
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
        # self.ip_address = ip
        # location = geolocate_ip(ip)
        # self.geo_location = f"{location['city']}, {location['country']}"
        self.anonymized_ip = anonymize_ip(ip)
        self.user_agent = user_agent
        self.user_id = user_id
    
    def __repr__(self):
        """How message is logged in the dev's console"""
        return f"<Activity log: {self.id} {self.level} {self.message}>"
    
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