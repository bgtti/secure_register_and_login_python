import logging
from flask_login import UserMixin
from datetime import datetime, timezone
from sqlalchemy import Enum
from app.extensions import db
from app.utils.constants.enum_class import UserFlag, modelBool
from app.utils.constants.account_constants import INPUT_LENGTH

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
    answered_by = db.Column(db.String(INPUT_LENGTH['email']['maxValue']), default="", nullable=True) # email of the admin who answered message
    answer_date = db.Column(db.DateTime, nullable=True) # date the answer was sent
    answer = db.Column(db.String(INPUT_LENGTH['contact_message']['maxValue']), default="", nullable=True) # content of the answer

    def __init__(self, sender_name, sender_email, subject, message, **kwargs):
        self.sender_name  = sender_name
        self.sender_email = sender_email
        self.subject = subject
        self.message = message
    
    def __repr__(self):
        return f"<New message: {self.sender_name} from {self.sender_email}>"
    
    def serialize_message_table(self):
        the_date = self.answer_date
        if the_date is None:
            the_date = ""
        return {
            "id": self.id,
            "date": self.date,
            "sender_is_user": self.user_id != 0,
            "sender_name": self.sender_name,
            "sender_email": self.sender_email,
            "subject": self.subject,
            "message": self.message,
            "flagged": self.flagged.value,
            "is_spam": self.is_spam.value,
            "answer_needed": self.answer_needed.value,
            "was_answered":self.was_answered.value,
            "answered_by": self.answered_by,
            "answer_date": the_date,
            "answer": self.answer
        }
    
    def message_answered(self, answered_by, answer, answer_date = datetime.now(timezone.utc)):
        """
        message_answered(answered_by: str, answer: str) -> void
        ------------------------------
        Records answer to a user's message.
        Two required arguments: the email of the admin who answered the message and the content of the answer (string).
        One optional argument: the date the message was answered.
        """
        self.answered_by = answered_by
        self.answer = answer
        self.answer_needed = modelBool.FALSE
        self.was_answered = modelBool.TRUE
        self.answer_date = answer_date

    
    def flag_change(self, flag_colour):
        """
        Changes the message flag to the appropriate colour.
        Accepts the colour as an argument: choices accepted are those in UserFlag Enum: red, yellow, purple, and blue.
        The argument flag_colour must be a string - upper or lower case.
        ------------------------------------------------
        Example usage:
        message.flag_change("yellow")
        """
        flag_colour = flag_colour.upper()
        flags = [member.name for member in UserFlag]
        if flag_colour in flags:
            self.flagged = UserFlag[flag_colour].value
        else:
            logging.error(f"Message flag could not be changed: wrong input for flag_change: {flag_colour}. Check UserFlag Enum for options.")
            print("Error: flag color not found. Message's flagged status not changed.")

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