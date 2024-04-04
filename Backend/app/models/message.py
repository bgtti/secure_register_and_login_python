import logging
from flask_login import UserMixin
from datetime import datetime, timezone
from sqlalchemy import Enum
from app.extensions import db
from app.utils.constants.enum_class import UserFlag
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
    message = db.Column(db.String(INPUT_LENGTH['contact_message']['maxValue']), nullable=False)
    flagged = db.Column(db.Enum(UserFlag), default=UserFlag.BLUE, nullable=False)

    def __init__(self, sender_name, sender_email, message, **kwargs):
        self.sender_name  = sender_name
        self.sender_email = sender_email
        self.message = message
    
    def __repr__(self):
        return f"<New message: {self.sender_name} from {self.sender_email}>"
    
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