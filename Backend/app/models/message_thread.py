"""
Docstring for Backend.app.models.message_thread


1) MessageThread (or Conversation)

Stores grouping + status.

Typical fields:

id

created_at, updated_at, last_message_at

subject (optional, or keep on first message)

status (open/pending/closed/spam)

flagged (your Flag enum)

customer_email (or user_id if authenticated)

assigned_to_admin_id (optional)

spam_score / is_spam (optional)

2) Message (timeline items)

Stores each inbound/outbound message.

Typical fields:

id

thread_id (FK → message_thread.id)

created_at

direction enum: INBOUND / OUTBOUND

sender_name, sender_email

recipient_email (optional)

body (message text)

channel enum: CONTACT_FORM, EMAIL, IN_APP

sent_by_admin_id (nullable)

delivery_status (optional: queued/sent/failed)

in_reply_to_message_id (optional) if you want reply chaining

This is the simplest structure that scales.
"""
# Python/Flask libraries
import secrets
import string
from datetime import datetime, timedelta, timezone

# Extensions and configurations
from flask_login import UserMixin
from app.extensions.extensions import db
from app.extensions.sqlalchemy_config import UTCDateTime

# Constants
from app.constants.validation_input_length import INPUT_LENGTH
from constants.message_and_thread import ThreadStatus, ThreadPriority
from app.constants.flags import Flag

############## MODEL ###############
class MessageThread(UserMixin, db.Model):
    """
    MessageThread groups messages into a conversation.

    Add thread like:
    ```
    thread = MessageThread(
        user_id = 29
        customer_email = jose@example.com
        customer_name = Jose Sanchez
    )
    db.session.add(thread)
    db.session.commit()
    ```
    """
    __tablename__ = "message_thread"
    # TABLE
    id = db.Column(db.Integer, primary_key=True, unique=True)
    # created_at = db.Column(UTCDateTime, default=datetime.now(timezone.utc), index=True, nullable=False)
    created_at = db.Column(UTCDateTime, default=lambda: datetime.now(timezone.utc), index=True, nullable=False)
    updated_at = db.Column(UTCDateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc), index=True, nullable=False) #auto-updates
    last_message_at = db.Column(UTCDateTime, default=lambda: datetime.now(timezone.utc), index=True, nullable=False)

    # THREAD TITLE and reference
    subject = db.Column(db.String(INPUT_LENGTH['contact_message_subject']['maxValue']), nullable=False)
    reference = db.Column(db.String(15), nullable=False, index=True, unique=True) #public reference, use generate_thread_reference function

    # STATUS (PUBLIC: VISIBLE TO USER)
    status = db.Column(db.Enum(ThreadStatus), default=ThreadStatus.NEW, index=True, nullable=False) # New, Open, Closed, etc

    # ADMIN FILTERING
    # answer_needed = db.Column(db.Boolean, default=True, index=True, nullable=False)
    priority = db.Column(db.Enum(ThreadPriority), default=ThreadPriority.NORMAL, index=True, nullable=False)
    flagged = db.Column(db.Enum(Flag), default=Flag.BLUE, nullable=False)
    is_spam = db.Column(db.Boolean, default=False, index=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, index=True, nullable=False) # to soft-delete message threads
    deleted_at = db.Column(UTCDateTime, nullable=True) #soft-delete (also change is_deleted)
    purge_date = db.Column(UTCDateTime, nullable=True) # date to automatically detele thread

    # OPTIONAL categorization / triage
    category = db.Column(db.String(50), nullable=True)  # e.g. "Billing", "Tech", "Account"

    # DETAILS of SENDER/USER who initiated the thread
    originator_user_id = db.Column(db.Integer, default=0, index=True, nullable=False)  # 0 for anonymous/contact form
    originator_email = db.Column(db.String(254), index=True, nullable=True)
    originator_name = db.Column(db.String(120), nullable=True)

    # STAFF ASSIGNED TO HANDLE IT
    assigned_to_admin_id = db.Column(db.Integer, nullable=True, index=True)

    # Relationship: thread -> messages
    messages = db.relationship(
        "Message",
        back_populates="thread",
        cascade="all, delete-orphan",
        order_by="Message.created_at.asc()",
        lazy="dynamic",
    )
    # Relationship: thread -> events 
    # events = db.relationship(
    #     "MessageThreadEvent",
    #     back_populates="thread",
    #     cascade="all, delete-orphan",
    #     order_by="MessageThreadEvent.created_at.asc()",
    #     lazy="dynamic",   # use .all(), .limit(), .order_by() queries
    # )
    # Relationship: thread -> notes
    notes = db.relationship(
        "MessageThreadNote",
        back_populates="thread",
        cascade="all, delete-orphan",
        order_by="MessageThreadNote.created_at.desc()",
        lazy="dynamic",
    ) 

    def __init__(self, originator_user_id, originator_email, originator_name, subject, reference, **kwargs):
        self.originator_user_id = originator_user_id
        self.originator_email = originator_email
        self.originator_name = originator_name
        self.subject = subject
        self.reference = reference #generate_thread_reference()
    
    def __repr__(self):
        return f"<Message Thread {self.id} initiated. User id: {self.originator_user_id}.>"

    # def touch_last_message(self, when=None):
    #     self.last_message_at = when or datetime.now(timezone.utc)
    #     self.updated_at = datetime.now(timezone.utc)

    # def mark_spam(self):
    #     self.is_spam = True
    #     self.status = ThreadStatus.SPAM
    #     self.answer_needed = False
    #     self.flagged = Flag.PURPLE  

    # def close(self):
    #     self.status = ThreadStatus.CLOSED
    #     self.answer_needed = False

    # def reopen(self):
    #     if self.status in {ThreadStatus.CLOSED, ThreadStatus.RESOLVED}:
    #         self.status = ThreadStatus.OPEN
    #     self.answer_needed = True

    # def serialize_thread_row(self):
    #     """For inbox/table view."""
    #     return {
    #         "id": self.id,
    #         "created_at": self.created_at,
    #         "updated_at": self.updated_at,
    #         "last_message_at": self.last_message_at,
    #         "status": self.status.value,
    #         "priority": self.priority.value,
    #         "category": self.category,
    #         "user_id": self.user_id,
    #         "customer_email": self.customer_email,
    #         "customer_name": self.customer_name,
    #         "assigned_to_admin_id": self.assigned_to_admin_id,
    #         "flagged": self.flagged if isinstance(self.flagged, str) else self.flagged.value,
    #         "is_spam": bool(self.is_spam),
    #         "answer_needed": bool(self.answer_needed),
    #     }
    # def trash_thread(thread: MessageThread, actor_staff_id: int):
    #     now = datetime.now(timezone.utc)
    #     thread.status = ThreadStatus.TRASHED
    #     thread.trashed_at = now
    #     thread.purge_after = now + timedelta(days=30)

    #     thread.events.append(MessageThreadEvent(
    #         actor_staff_id=actor_staff_id,
    #         event_type=ThreadEventType.MOVED_TO_TRASH,
    #         from_value="ACTIVE",
    #         to_value="TRASHED",
    #         description="Thread moved to trash (scheduled for purge)."
    #     ))
    # def restore_thread(thread: MessageThread, actor_staff_id: int):
    #     thread.status = ThreadStatus.OPEN  # or previous status if you stored it
    #     thread.trashed_at = None
    #     thread.purge_after = None
    #     thread.events.append(MessageThreadEvent(
    #         actor_staff_id=actor_staff_id,
    #         event_type=ThreadEventType.RESTORED_FROM_TRASH,
    #         from_value="TRASHED",
    #         to_value="OPEN",
    #         description="Thread restored from trash."
    #     ))

# schedule cron/automated job to purge deleted threads automatically like:
# def purge_trashed_threads():
#     now = datetime.now(timezone.utc)
#     threads = (MessageThread.query
#                .filter(MessageThread.status == ThreadStatus.TRASHED)
#                .filter(MessageThread.purge_after <= now)
#                .all())

#     for t in threads:
#         db.session.delete(t)  # cascades to messages/events/notes if you set cascades
#     db.session.commit()