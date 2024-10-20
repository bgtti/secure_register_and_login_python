import ast
from app.config import ADMIN_ACCT
from app.extensions import db
from app.models.user import User
from app.models.message import Message
from app.dummie_data.create_files import generate_fake_mail
from app.extensions import faker

# Data for Admin Account (to mark messages as answered):
ADMIN_DATA = ast.literal_eval(ADMIN_ACCT)
ADMIN_EMAIL = ADMIN_DATA[1]

"""
This file contains the create_dummie_mesages function, which can be called to create dummie messages in the db for testing and visualization. This should simulate the receiving of messages through the contact form (without forwarding them to the specified administrator email address).
Currently used in dummie_users.py after dummie users are inserted to the db.
"""

def create_spam_messages():
    """
    Creates 2 spam messages, adding them to the database.
    Used in create_dummie_messages.
    """
    spams = [
        ("Brain enlargement offer", "Only at Spam Brain can you get 20% off your brain enlargent surgery today! Signup now at getmybrainlarger.com !"),
        ("Grow your user base", "Want more users? Tired of working hard to chase subscribers? Amram Johnson can help you! For a mere 1'000 USD you can get 5 new subscribers this month! Respond to this email with I WANT MORE USERS today!")
    ]
    for subject, message in spams:
        sender_name = faker.name()
        sender_email= generate_fake_mail(sender_name)
        new_spam = Message(sender_name=sender_name, sender_email=sender_email, subject=subject, message=message)
        db.session.add(new_spam)
        new_spam.mark_spam()
        
    db.session.commit()

def create_message_unkown_sender():
    """
    Creates a message from an unknown sender, adding it to the database.
    Used in create_dummie_messages.
    """
    sender_name = faker.name()
    sender_email= generate_fake_mail(sender_name)
    subject = "Cannot create account"
    message = f"Hi, my name is {sender_name}, and I keep getting an error when trying to sign up. Can you help?"

    new_message = Message(sender_name=sender_name, sender_email=sender_email, subject=subject, message=message)
    db.session.add(new_message)
    db.session.commit()


def create_dummie_messages():
    """
    Creates 26 dummie user messages, 23 of which can be linked to a dummie user by id.
    Messages are created and inserted to the Message db.
    Should be used in the create_dummie_user_accts function, after dummie users are created.
    """
    users = User.query.order_by(User.created_at.desc()).limit(23).all()

    for i, user in enumerate(users):
        subject = faker.text(max_nb_chars=25)
        message = faker.text(max_nb_chars=90)
        new_message = Message(sender_name=user.name, sender_email=user.email, subject=subject, message=message)
        new_message.user_id=user.id
        new_message.date=user.last_seen
        db.session.add(new_message)

        if i < 19:  # Mark as no reply needed for the first 19 messages
            new_message.no_reply_needed()
        elif 19 <= i < 22:  # Mark as answered for the subsequent 3 messages
            answered_by = ADMIN_EMAIL
            answer = faker.text(max_nb_chars=70)
            new_message.message_answered(answered_by, answer)
        # For the last message added, no change is needed.
        
    db.session.commit()
    create_message_unkown_sender()
    create_spam_messages()


