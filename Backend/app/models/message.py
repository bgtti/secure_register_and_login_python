"""
`models/message.py` contains:

**Message** class (the db model) which stores messages sent to the app via contact form

how message works:
1) create a thread
2) add message to thread
4) optional: add notes to thread
5) if someone changes message thread: add thread event to thread




How it works in practice
Contact form submission
thread = MessageThread(
    user_id=0,
    customer_email=email,
    customer_name=name,
)
db.session.add(thread)
db.session.flush()

message = Message(
    thread_id=thread.id,
    direction=MessageDirection.INBOUND,
    channel=MessageChannel.CONTACT_FORM,
    subject=subject,
    body=message_text,
    sender_name=name,
    sender_email=email,
    user_agent=request.user_agent.string,
    ip_address=request.remote_addr,
)

thread.last_message_at = message.created_at
thread.answer_needed = True

db.session.add(message)
db.session.commit()


Admin reply
message = Message(
    thread_id=thread.id,
    direction=MessageDirection.OUTBOUND,
    channel=MessageChannel.EMAIL,
    subject="Re: " + original_subject,
    body=reply_text,
    author_staff_id=admin.id,
    author_staff_name=admin.name,
    author_staff_email=admin.email,
)

thread.status = ThreadStatus.WAITING_ON_CUSTOMER
thread.answer_needed = False
thread.last_message_at = message.created_at

db.session.add(message)
db.session.commit()
"""
# Python/Flask libraries
import logging
import re
from flask_login import UserMixin
from datetime import datetime, timezone

# Extensions and configurations
from sqlalchemy import Enum
from utils.print_to_terminal import print_to_terminal
from config.values import EMAIL_CREDENTIALS
from app.extensions.extensions import db
from app.extensions.sqlalchemy_config import EncryptedType, UTCDateTime

# Constants 
from app.constants.flags import Flag
from app.constants.validation_input_length import INPUT_LENGTH
from app.constants.validation_patterns import EMAIL_PATTERN
from app.constants.message_and_thread import MessageDirection, MessageChannel

# Helpers
from app.common.enum_helpers import map_string_to_enum


class Message(UserMixin, db.Model):
    """
    Messages received through the contact form.
    (routes in the "contact" module)
    --------------------------------------------
    Example usage for contact_form:
    new_message = Message(sender_name="joe", sender_email="joe@fakemail.com", message="hello world")
    """
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    # date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    created_at = db.Column(UTCDateTime, default=lambda: datetime.now(timezone.utc), index=True, nullable=False)

    # --- Sender info (for inbound or outbound messages) ---
    sender_name = db.Column(db.String(INPUT_LENGTH['name']['maxValue']), nullable=False)
    sender_email = db.Column(db.String(INPUT_LENGTH['email']['maxValue']), nullable=False)
    sender_id = db.Column(db.Integer, default=0, index=True, nullable=False)  # 0 = anonymous

    # --- Recipient info
    recipient_id = db.Column(db.Integer, default=0, index=True, nullable=False)  # 0 = system
    recipient_email = db.Column(db.String(INPUT_LENGTH['email']['maxValue']), nullable=True)
    recipient_name = db.Column(db.String(INPUT_LENGTH['name']['maxValue']), nullable=True)
    marked_read_by_recipient = db.Column(db.Boolean, default=False, nullable=False)

    # --- Content ---
    subject = db.Column(db.String(INPUT_LENGTH['contact_message_subject']['maxValue']), nullable=False)
    body = db.Column(db.String(INPUT_LENGTH['contact_message']['maxValue']), nullable=False)

    # --- Admin Tags ---
    marked_read_by_admin = db.Column(db.Boolean, default=False, nullable=False)
    marked_read_by_admin_id = db.Column(db.Integer, nullable=True)
    direction = db.Column(db.Enum(MessageDirection), nullable=False, index=True)

    # --- System Tags ---
    channel = db.Column(db.Enum(MessageChannel), nullable=False, index=True)

    # --- Sender Optional metadata (source/fingerprinting) ---
    ip_address = db.Column(EncryptedType, nullable=True)
    geo_location = db.Column(EncryptedType, nullable=True)
    user_agent = db.Column(db.String(250), nullable=True)

    # --- Relationship ---
    thread_id = db.Column(
        db.Integer,
        db.ForeignKey("message_thread.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    thread = db.relationship("MessageThread", back_populates="messages")

    # answer_needed = db.Column(db.Boolean, default=True, nullable=False)
    # was_answered = db.Column(db.Boolean, default=False, nullable=False)
    # answered_by = db.Column(db.String(INPUT_LENGTH['email']['maxValue']), default="", nullable=True) # email of the admin who answered message or email of the main account used to set up system messaging
    # answerer_name = db.Column(db.String(INPUT_LENGTH['name']['maxValue']), default="", nullable=True) # name of the admin who answered message
    # answerer_id = db.Column(db.Integer, nullable=True) # id of the admin who answered message
    # answer_date = db.Column(db.DateTime, nullable=True) # date the answer was sent (as input by admin if answer was recorded)
    # answer_subject = db.Column(db.String(INPUT_LENGTH['contact_message_subject']['maxValue']), default="", nullable=True) # subject of the answer
    # answer = db.Column(db.String(INPUT_LENGTH['contact_message']['maxValue']), default="", nullable=True) # content of the answer
    # answer_recorded_at = db.Column(db.DateTime, nullable=True) # date the answer was recorded in the system

    # def __init__(self, sender_name, sender_email, subject, message, **kwargs):
    #     self.sender_name  = sender_name
    #     self.sender_email = sender_email
    #     self.subject = subject
    #     self.message = message

    def __init__(
        self,
        thread_id,
        direction,
        channel,
        body,
        subject=None,
        sender_name=None,
        sender_email=None,
        user_id=0,
        user_agent=None,
        ip_address=None,
        geo_location=None,
        recipient_id=0,
        recipient_email=None,
        recipient_name=None,
        **kwargs
    ):
        self.thread_id = thread_id
        self.direction = direction
        self.channel = channel
        self.body = body
        self.subject = subject

        self.sender_name = sender_name
        self.sender_email = sender_email
        self.user_id = user_id

        self.user_agent = user_agent
        self.ip_address = ip_address

        self.recipient_id=recipient_id,
        self.recipient_email=recipient_email,
        self.recipient_name=recipient_name,

    def __repr__(self):
        return f"<New message {self.id} thread={self.thread_id} from {self.sender_email}>"
    
    # def serialize(self): TODO
    #     return {
    #         "id": self.id,
    #         "created_at": self.created_at,
    #         "direction": self.direction.value,
    #         "channel": self.channel.value,
    #         "subject": self.subject,
    #         "body": self.body,
    #         "sender_name": self.sender_name,
    #         "sender_email": self.sender_email,
    #         "author_staff_id": self.author_staff_id,
    #         "author_staff_name": self.author_staff_name,
    #     }
    
    # def serialize_message_table(self):
    #     answer_date = self.answer_date if self.answer_date is not None else ""
    #     answer_needed = self.answer_needed.value == "true"
    #     is_spam = self.is_spam.value == "true"
    #     was_answered = self.was_answered.value == "true"
    #     return {
    #         "id": self.id,
    #         "date": self.date,
    #         "sender_is_user": self.user_id != 0,
    #         "user_id": self.user_id,
    #         "sender_name": self.sender_name,
    #         "sender_email": self.sender_email,
    #         "subject": self.subject,
    #         "message": self.message,
    #         "flagged": self.flagged.value,
    #         "is_spam": is_spam,
    #         "answer_needed": answer_needed ,
    #         "was_answered":was_answered,
    #         "answered_by": self.answered_by,
    #         "answer_date": answer_date,
    #         "answer": self.answer
    #     }
    # answered_by = db.Column(db.String(INPUT_LENGTH['email']['maxValue']), default="", nullable=True) # email of the admin who answered message or email of the main account used to set up system messaging
    # answerer_name = db.Column(db.String(INPUT_LENGTH['name']['maxValue']), default="", nullable=True) # name of the admin who answered message
    # answerer_id = db.Column(db.Integer, nullable=True) # id of the admin who answered message
    # answer_date = db.Column(db.DateTime, nullable=True) # date the answer was sent
    # answer_subject = db.Column(db.String(INPUT_LENGTH['contact_message_subject']['maxValue']), default="", nullable=True) # subject of the answer
    # answer = db.Column(db.String(INPUT_LENGTH['contact_message']['maxValue']), default="", nullable=True) # content of the answer
    
    def record_answer(self, answered_by, answerer_name, answerer_id, answer, answer_date= datetime.now(timezone.utc), answer_subject="Re: message"):
        """
        record_answer(answered_by: str, answerer_name:str, answerer_id: int, answer: str) -> void
        ------------------------------
        Records answer to a user's message.
        Should be used to record answers that were NOT sent through the app by email.
        Required arguments: the email, name, and id of the admin who answered the message and the content of the answer (string).
        Optional arguments: the date the message was answered and the answer subject.
        """
        self.answered_by = answered_by
        self.answerer_name = answerer_name
        self.answerer_id = answerer_id
        self.answer_subject = answer_subject
        self.answer = answer
        self.answer_needed = False
        self.was_answered = True
        self.answer_date = answer_date
        self.answer_recorded_at= datetime.now(timezone.utc)
    
    def email_answer(self, answerer_name, answerer_id, answer, answer_subject="Re: message"):
        """
        record_answer(answerer_name:str, answerer_id: int, answer: str) -> void
        ------------------------------
        Records answer to a user's message per email.
        Should be used to record answers that were sent through the app by email.
        Required arguments: name and id of the admin who answered the message and the content of the answer (string).
        Optional argument: the answer subject.
        """
        if not EMAIL_CREDENTIALS["email_set"]:
            logging.warning(f"No email was set for this app. Default/fake mail address being used to add email answer to db.")
        self.answered_by = EMAIL_CREDENTIALS["email_address"]
        self.answerer_name = answerer_name
        self.answerer_id = answerer_id
        self.answer_subject = answer_subject
        self.answer = answer
        self.answer_needed = False
        self.was_answered = True
        self.answer_date = datetime.now(timezone.utc)
        self.answer_recorded_at= datetime.now(timezone.utc)

    
    def flag_change(self, flag_colour):
        """
        Changes the message flag to the appropriate colour.
        Accepts the colour as an argument: choices accepted are those in Flag Enum: red, yellow, purple, and blue.
        The argument flag_colour must be a string - upper or lower case.
        ------------------------------------------------
        Example usage:
        message.flag_change("yellow")
        """
        the_colour = flag_colour.lower()
        flag = map_string_to_enum(the_colour, Flag)
        if flag is not None:
            self.flagged = flag
        else:
            logging.error(f"Message flag could not be changed: wrong input for flag_change: {flag_colour}. Check Flag Enum for options.")
            print_to_terminal("Error (message method flag_change): flag color not found. Message's flagged status not changed.")

    def mark_spam(self):
        """
        Marks a message as spam. 
        This will change the flag colour of the message, it will mark answer_needed as false, and is_spam as true.
        PS: It will not mark the sender of the message as a spammer.
        ------------------------------------------------
        Example usage:
        # ...
        message.mark_spam()
        db.session.commit()
        """
        self.flagged = Flag.RED
        self.answer_needed = False
        self.is_spam = True
    
    def no_reply_needed(self):
        """
        Marks a message as 'no reply needed' by setting answer_needed to false. 
        ------------------------------------------------
        Example usage:
        # ...
        message.no_reply_needed()
        db.session.commit()
        """
        self.answer_needed = False

    def reply_needed(self):
        """
        Marks a message as 'reply needed' by setting answer_needed to true. 
        ------------------------------------------------
        Example usage:
        # ...
        message.reply_needed()
        db.session.commit()
        """
        self.answer_needed = True