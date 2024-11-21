import logging
from flask_login import UserMixin
from datetime import datetime, timezone
from sqlalchemy import Enum
from app.extensions.extensions import db
from app.utils.constants.enum_class import UserFlag, modelBool
from app.utils.constants.account_constants import INPUT_LENGTH

# List of senders marked as spammers

# TO-DO:
# If someone creates an account from list of spammers: automatically block user?
# If current user is marked as spammer: block user?

class Spammer(UserMixin, db.Model):
    """
    Users marked as spammers.
    (by an admin user)
    --------------------------------------------
    Example usage:
    new_spammer = Spammer(sender_name="joe", sender_email="joe@fakemail.com", message="hello world")
    """
    __tablename__ = "spammer"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))#when sender was marked as spammer
    admin_id = db.Column(db.Integer, default=0) #who marked the sender as spammer
    sender_email = db.Column(db.String(INPUT_LENGTH['email']['maxValue']), nullable=False)

    def __init__(self, admin_id, sender_email, **kwargs):
        self.admin_id  = admin_id
        self.sender_email = sender_email
    
    def __repr__(self):
        return f"<New spammer: {self.sender_email}>"