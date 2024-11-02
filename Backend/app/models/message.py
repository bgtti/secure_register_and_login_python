import logging
import re
from flask_login import UserMixin
from datetime import datetime, timezone
from sqlalchemy import Enum
from app.config import EMAIL_CREDENTIALS
from app.extensions import db
from app.utils.constants.enum_class import UserFlag, modelBool
from app.utils.constants.account_constants import INPUT_LENGTH
from app.utils.constants.enum_helpers import map_string_to_enum
from app.utils.console_warning.print_warning import console_warn
from app.utils.constants.account_constants import EMAIL_PATTERN

# Saves messages sent through the contact form

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
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, default=0) #if message from registered user, save id
    sender_name = db.Column(db.String(INPUT_LENGTH['name']['maxValue']), nullable=False)
    sender_email = db.Column(db.String(INPUT_LENGTH['email']['maxValue']), nullable=False)
    subject = db.Column(db.String(INPUT_LENGTH['contact_message_subject']['maxValue']), nullable=False)
    message = db.Column(db.String(INPUT_LENGTH['contact_message']['maxValue']), nullable=False)
    flagged = db.Column(db.Enum(UserFlag), default=UserFlag.BLUE, nullable=False)
    is_spam = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False)
    answer_needed = db.Column(db.Enum(modelBool), default=modelBool.TRUE, nullable=False)
    was_answered = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False)
    answered_by = db.Column(db.String(INPUT_LENGTH['email']['maxValue']), default="", nullable=True) # email of the admin who answered message or email of the main account used to set up system messaging
    answerer_name = db.Column(db.String(INPUT_LENGTH['name']['maxValue']), default="", nullable=True) # name of the admin who answered message
    answerer_id = db.Column(db.Integer, nullable=True) # id of the admin who answered message
    answer_date = db.Column(db.DateTime, nullable=True) # date the answer was sent (as input by admin if answer was recorded)
    answer_subject = db.Column(db.String(INPUT_LENGTH['contact_message_subject']['maxValue']), default="", nullable=True) # subject of the answer
    answer = db.Column(db.String(INPUT_LENGTH['contact_message']['maxValue']), default="", nullable=True) # content of the answer
    answer_recorded_at = db.Column(db.DateTime, nullable=True) # date the answer was recorded in the system

    def __init__(self, sender_name, sender_email, subject, message, **kwargs):
        self.sender_name  = sender_name
        self.sender_email = sender_email
        self.subject = subject
        self.message = message
    
    def __repr__(self):
        return f"<New message: {self.sender_name} from {self.sender_email}>"
    
    def serialize_message_table(self):
        answer_date = self.answer_date if self.answer_date is not None else ""
        answer_needed = self.answer_needed.value == "true"
        is_spam = self.is_spam.value == "true"
        was_answered = self.was_answered.value == "true"
        return {
            "id": self.id,
            "date": self.date,
            "sender_is_user": self.user_id != 0,
            "user_id": self.user_id,
            "sender_name": self.sender_name,
            "sender_email": self.sender_email,
            "subject": self.subject,
            "message": self.message,
            "flagged": self.flagged.value,
            "is_spam": is_spam,
            "answer_needed": answer_needed ,
            "was_answered":was_answered,
            "answered_by": self.answered_by,
            "answer_date": answer_date,
            "answer": self.answer
        }
    answered_by = db.Column(db.String(INPUT_LENGTH['email']['maxValue']), default="", nullable=True) # email of the admin who answered message or email of the main account used to set up system messaging
    answerer_name = db.Column(db.String(INPUT_LENGTH['name']['maxValue']), default="", nullable=True) # name of the admin who answered message
    answerer_id = db.Column(db.Integer, nullable=True) # id of the admin who answered message
    answer_date = db.Column(db.DateTime, nullable=True) # date the answer was sent
    answer_subject = db.Column(db.String(INPUT_LENGTH['contact_message_subject']['maxValue']), default="", nullable=True) # subject of the answer
    answer = db.Column(db.String(INPUT_LENGTH['contact_message']['maxValue']), default="", nullable=True) # content of the answer
    
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
        self.answer_needed = modelBool.FALSE
        self.was_answered = modelBool.TRUE
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
        self.answer_needed = modelBool.FALSE
        self.was_answered = modelBool.TRUE
        self.answer_date = datetime.now(timezone.utc)
        self.answer_recorded_at= datetime.now(timezone.utc)

    
    def flag_change(self, flag_colour):
        """
        Changes the message flag to the appropriate colour.
        Accepts the colour as an argument: choices accepted are those in UserFlag Enum: red, yellow, purple, and blue.
        The argument flag_colour must be a string - upper or lower case.
        ------------------------------------------------
        Example usage:
        message.flag_change("yellow")
        """
        the_colour = flag_colour.lower()
        flag = map_string_to_enum(the_colour, UserFlag)
        if flag is not None:
            self.flagged = flag
        else:
            logging.error(f"Message flag could not be changed: wrong input for flag_change: {flag_colour}. Check UserFlag Enum for options.")
            console_warn("Error (message method flag_change): flag color not found. Message's flagged status not changed.")

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
        self.flagged = UserFlag.RED
        self.answer_needed = modelBool.FALSE
        self.is_spam = modelBool.TRUE
    
    def no_reply_needed(self):
        """
        Marks a message as 'no reply needed' by setting answer_needed to false. 
        ------------------------------------------------
        Example usage:
        # ...
        message.no_reply_needed()
        db.session.commit()
        """
        self.answer_needed = modelBool.FALSE

    def reply_needed(self):
        """
        Marks a message as 'reply needed' by setting answer_needed to true. 
        ------------------------------------------------
        Example usage:
        # ...
        message.reply_needed()
        db.session.commit()
        """
        self.answer_needed = modelBool.TRUE