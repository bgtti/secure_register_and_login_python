from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

# level refers to the level in the logging module (INFO, CRITICAL, ETC) while type is self-defined log level.
# more information about log events are in utils>log_event_utils
# that is where log_event logic resides

class LogEvent(UserMixin, db.Model):
    __tablename__ = "log_event"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    level = db.Column(db.Integer, default=20)
    type = db.Column(db.String(50), nullable=False)
    activity = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    session_id = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    def __init__(self, level, type, activity, message, session_id, **kwargs):
        self.level = level
        self.type = type
        self.activity = activity
        self.message = message
        self.session_id = session_id
        self.created_at = datetime.utcnow()
    
    def __repr__(self):
        return f"<Log: {self.id} {self.type} {self.message}>"