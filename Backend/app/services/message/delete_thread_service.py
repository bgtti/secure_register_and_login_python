# Python/Flask libraries
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import logging

# Extensions and configurations
from app.extensions.extensions import db

# Models
from app.models.message_thread import MessageThread

def svc_delete_thread(thread: MessageThread, delete: bool, commit: bool = True) -> bool:
    """
    Thread can be soft-deleted (marked for deletion), deleted (along with its messages), or moved back to inbox (if it had been soft deleted before).

    Set delete to False if the thread should be moved back to inbox.
    If delete is True and thread.is_deleted is False, it will set it to True and add a deletion and purge date.
    If delete is True and thread.is_deleted is True, it will effectively remove the Thread from the DB.
    If delete is False and thread.is_deleted is False, the request will be ignored and the function will just return True.

    :param thread (MessageThread): member of MessageThread model.
    :param delete (bool): True if want to delete thread, False otherwise. 
    :param commit (bool): True if want the changes to be committed to DB (select False if the caller is another service).
    """
    if not thread or not getattr(thread, "id", None) or not isinstance(delete, bool):
        logging.error("Invalid parameters passed to svc_delete_thread.")
        return False

    try:
        # Soft delete thread 
        if not thread.is_deleted and delete:
            thread.is_deleted = True
            thread.deleted_at = datetime.now(timezone.utc)
            one_year_from_now = datetime.now(timezone.utc) + relativedelta(years=1) # accounts for leap years, and years that dont have 365 days
            thread.purge_date = one_year_from_now 

        # Bring soft-deleted thread back to inbox
        elif thread.is_deleted and not delete:
            thread.is_deleted = False
            thread.deleted_at = None
            thread.purge_date = None

        # If the thread is soft-deleted, purge along with all messages
        elif thread.is_deleted and delete:
            db.session.delete(thread)
            logging.info(f"Thread {thread.id} will be purged.")

        # not thread.is_deleted and not delete
        else:
            return True

        if commit:
            db.session.commit()

        return True
    
    except Exception as e:
        if commit:
            db.session.rollback()
        logging.error(f"svc_delete_thread was unable to mark thread for deletion. Error: {e}")
        return False