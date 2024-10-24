from app.models.spammer import Spammer
from sqlalchemy.exc import IntegrityError
import logging
from app.extensions import db

def set_spammer(admin_id, spammer_email):
    """
    mark_message_as(admin_id: int, spammer_email: str) -> bool
    ----------------------------------------------------------
    Adds an email to the Spammer database.
    Takes the id of the admin doing the action and the spammer's email as arguments.
    
    Returns:
        True if the spammer is added successfully or email already in spammer's list.
        False if there is an error or integrity error.
    """
    try:
        # Check if spammer is already in the database
        existing_spammer = Spammer.query.filter_by(sender_email=spammer_email).first()
        if existing_spammer:
            logging.info(f"Email {spammer_email} already exists in Spammer list.")
            return True

        # Create a new spammer entry
        new_spammer = Spammer(admin_id=admin_id, sender_email=spammer_email)
        db.session.add(new_spammer)
        db.session.commit()

        logging.info(f"Email {spammer_email} added to Spammer list by admin {admin_id}.")
        return True

    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"Integrity error when adding email {spammer_email} to spammer list: {e}")
        return False

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error when adding email {spammer_email} to spammer list: {e}")
        return False