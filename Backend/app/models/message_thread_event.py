"""
Docstring for Backend.app.models.message_thread_event
"""
# Python/Flask libraries
from datetime import datetime, timezone

# Extensions and configurations
from flask_login import UserMixin
from app.extensions.extensions import db
from app.extensions.sqlalchemy_config import UTCDateTime

# Constants
from constants.message_and_thread import ThreadEventType

# TODO: delete????

# class MessageThreadEvent(db.Model):
#     """
#     Add event to thread like:
#     ```
#     event = MessageThreadEvent(
#         thread_id=22,
#         staff_id=15,
#         event_type=ThreadEventType.STATUS_CHANGED,
#         from_value=ThreadEventType.OPEN.value,
#         to_value=ThreadEventType.CLOSED.value
#     )
#     db.session.add(event)
#     db.session.commit()
#     ```
#     Or via append:
#     ```
#     thread.events.append(MessageThreadEvent(...))
#     db.session.commit()
#     ```
#     """
#     __tablename__ = "message_thread_event"
#     id = db.Column(db.Integer, primary_key=True)
#     # created_at = db.Column(UTCDateTime, default=datetime.now(timezone.utc), index=True, nullable=False)
#     created_at = db.Column(UTCDateTime, default=lambda: datetime.now(timezone.utc), index=True, nullable=False)

#     # User id of staff member who changed thread
#     staff_id = db.Column(db.Integer, nullable=False, index=True)  # 0 = system

#     # Event details
#     event_type = db.Column(db.Enum(ThreadEventType), nullable=False, index=True)
#     from_value = db.Column(db.String(120), nullable=True)
#     to_value = db.Column(db.String(120), nullable=True)

#     # Event description (what is sent to FE)
#     description = db.Column(db.String(250), nullable=True)  

#     # RELATIONSHIP
#     thread_id = db.Column(db.Integer, db.ForeignKey("message_thread.id", ondelete="CASCADE"), index=True, nullable=False)
#     thread = db.relationship("MessageThread", back_populates="events")

#     def __init__(self, staff_id, event_type, from_value, to_value, thread_id, description, **kwargs):
#         self.staff_id = staff_id
#         self.event_type = event_type
#         self.from_value = from_value
#         self.to_value = to_value
#         self.description = description
#         self.thread_id = thread_id
    
#     def __repr__(self):
#         return f"<Thread event {self.id} added to thread {self.thread_id} by {self.staff_id}.>"