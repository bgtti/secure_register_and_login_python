"""
Docstring for Backend.app.models.message_thread_note
"""
# Python/Flask libraries
from datetime import datetime, timedelta, timezone

# Extensions and configurations
from flask_login import UserMixin
from app.extensions.extensions import db
from app.extensions.sqlalchemy_config import UTCDateTime

class MessageThreadNote(db.Model):
    """
    Internal staff/system note attached to a MessageThread.

    Notes are not customer-facing messages. They are intended for
    admin/support use, triage, reminders, internal context, or
    automatic system annotations.

    Example:

    ```python
    note = MessageThreadNote(
        staff_id=20,
        body="User concern to be checked with dev team by Lucy.",
        is_pinned=True,
        thread_id=22,
    )

    db.session.add(note)
    db.session.commit()
    ```
    """
    __tablename__ = "message_thread_note"
    id = db.Column(db.Integer, primary_key=True)
    # created_at = db.Column(UTCDateTime, default=datetime.now(timezone.utc), index=True, nullable=False)
    created_at = db.Column(UTCDateTime, default=lambda: datetime.now(timezone.utc), index=True, nullable=False)
    updated_at = db.Column(UTCDateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc), index=True, nullable=False)

    staff_id = db.Column(db.Integer, nullable=False, index=True) # user id of staff member who authored note or 0 for 'system'
    body = db.Column(db.Text, nullable=False)
    is_pinned = db.Column(db.Boolean, default=False, nullable=False)

    # RELATIONSHIP
    thread_id = db.Column(db.Integer, db.ForeignKey("message_thread.id", ondelete="CASCADE"), index=True, nullable=False)
    thread = db.relationship("MessageThread", back_populates="notes")

    def __init__(self, staff_id, body, thread_id, is_pinned=False, **kwargs):
        self.staff_id = staff_id
        self.body = body
        self.thread_id = thread_id
        self.is_pinned = is_pinned
    
    def __repr__(self):
        return f"<Note {self.id} added to thread {self.thread_id} by {self.staff_id}.>"