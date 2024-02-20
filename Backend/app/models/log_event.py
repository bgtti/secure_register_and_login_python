from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin
from datetime import datetime
from app.extensions import db

# TODO: create function to delete old logs on a schedule

# NOTE ABOUT THE DESIGN CHOICE OF HAVING BOTH LOG IN FILES AND (SOME) LOGS STORED IN A DB
#
# System logs are configured in the app's config file and saved in files inside the folder system_logs. These can include logs about events and issues that are essential to understand the behaviour of the application and debug issues.
# LogEvent are logs directly related to user activity (logging in) or actions (getting blocked by admin). These are kept in a database since it can be relevant for an admin to understand a problem the user might be facing or possibly causing.
# It is possible (and - from this developer's point of view - desirable) that something is both logged in a system log file as well as in LogEvent -- this redundancy might save information in case of a data loss for some reason (for intance, a problem with file rotation in the system logs or a database failure when logging to LogEvent).
# 

# NOTE ABOUT DESIGN CHOICE IN DB LOG EVENT
#
# The user table and the log_event table are not linked (eg: by foreign key): this was a design choice which you might consider silly and are welcome to change.
# The reason behind it was to make it a tiny bit harder to link an individual to any information that could be used to monitor his/her activity. In the case either table is compromised by a bad actor, the other would not be necessarily compromised.
# LogEvents can be liked to a user when the user's uuid is known - and the only route currently linking a user to his/her logs is admin_user_logs > where only an administrator should be able to pull this information in case it helps them answer a user's question or give more insight about what the user was doing when a problem ocurred. 
# If a user is deleted, a LogEvent will not be deleted automatically => but it will no longer be possible to link an EventLog to a user.
# Sensitive information should not be logged, and logs on their ow
# A system to standardize db logs was created and resides in utils>log_event_utils. log_event is the function that should be used to log into the db. Constants.py contain the terminology used in the different log-type files (eg: log_event_login), each file defining possible outcomes in a route and assigning a code to it. A summary of all activities triggering logs are in log_event_activities_all.py. This was not only created for standardtization and diminishing the possibility for human error when logging - but the organization also helps to create a mental model of what outcomes to expect from an event as it relates to the user. 

class LogEvent(UserMixin, db.Model):
    """
    Use LogEvent to log user activity that would be relevant for debugging a problem the user might have encountered.
    Important: only log events using the log_event function available at utils>log_event_utils>log.py to keep log format standartized!
    ----------------------------------------------------
    Difference between type and level:
    level refers to the level as it would be in the logging module (INFO, CRITICAL, ETC)
    types are defined in utils>log_event_utils>constanty.py to define the log's importance as would be relevant to an admin. In this way, type is a self-defined log level that can be changed in the LOG_EVENT_TYPE 'enum'.
    ----------------------------------------------------
    Example usage for adding to this db:
    from app.utils.log_event_utils.log import log_event
    log_event("LOG_EVENT_LOGIN", "LEL_02")
    """
    __tablename__ = "log_event"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    level = db.Column(db.Integer, default=20)
    type = db.Column(db.String(50), nullable=False)
    activity = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    user_uuid = db.Column(db.String(32), nullable=False, default="none", index=True) # DELETE
    user_id = db.Column(db.Integer, nullable=True, index=True, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), index=True)
    
    def __init__(self, level, type, activity, message, **kwargs):
        self.level = level
        self.type = type
        self.activity = activity
        self.message = message
    
    def __repr__(self):
        return f"<Log: {self.id} {self.type} {self.message}>"
    
    def serialize_user_logs(self):
        return {
            "user_id": self.user_id,
            "created_at": self.created_at,
            "type": self.type,
            "activity": self.activity,
            "message": self.message,
        }