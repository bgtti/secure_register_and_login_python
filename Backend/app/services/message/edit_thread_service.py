# Python/Flask libraries
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import logging

# Extensions and configurations
from app.extensions.extensions import db

# Constants 
from app.constants.flags import Flag
from app.constants.message_and_thread import ThreadStatus, ThreadPriority

# Utilities
from app.common.enum_helpers.map_string_to_enum import map_string_to_enum

# Models
from app.models.message_thread import MessageThread


def svc_set_thread_is_spam(thread: MessageThread, is_spam: bool, commit: bool = True) -> bool:
    """
    Will mark thread.is_spam to True or False. Optionally, commits changes to the DB.
    If thread is spam, thread status will be changed to ThreadStatus.UNDER_REVIEW. These changes will not be reverted if thread.is_spam is marked as false.
    If thread is spam, a purge date will be added. It will be removed if thread.is_spam is set to 'False'.

    :param thread (MessageThread): member of MessageThread model.
    :param is_spam (bool): True if the thread is to be marked as spam, False otherwise.
    :param commit (bool): True if want the changes to be committed to DB (select False if the caller is another service).
    """
    if not thread or not getattr(thread, "id", None) or not isinstance(is_spam, bool):
        logging.error("Invalid parameters passed to svc_set_thread_is_spam.")
        return False
    try:
        thread.is_spam = is_spam
        thread.status = ThreadStatus.UNDER_REVIEW 
        if is_spam:
            one_year_from_now = datetime.now(timezone.utc) + relativedelta(years=1) # accounts for leap years, and years that dont have 365 days
            thread.purge_date = one_year_from_now 
        else:
            thread.purge_date = None
        if commit:
            db.session.commit()
        return True
    except Exception as e:
        if commit:
            db.session.rollback()
        logging.error(f"svc_set_thread_is_spam was unable to mark thread.is_spam. Error: {e}")
        return False

def svc_change_thread_flag(thread: MessageThread, flag_colour: str | Flag, commit: bool = True) -> bool:
    """
    Changes the message thread flag to the specified colour and optionally commits the changes to the DB.
    Accepts a flag color as an argument (as defined in the Flag Enum). Returns True if successful, False otherwise.

    :param thread (MessageThread): member of MessageThread model.
    :param flag_colour (str | Flag): The desired flag color (lower-case or enum).
    :param commit (bool): True if want the changes to be committed to DB (select False if the caller is another service).
    """
    if not thread or not getattr(thread, "id", None):
        logging.error("Invalid or no thread passed to svc_change_thread_flag.")
        return False
    
    flag = map_string_to_enum(flag_colour, Flag)
    if not flag:
        logging.error("Invalid flag parameters passed to svc_change_thread_flag.")
        return False
    
    try:
        if thread.flagged == flag:
            return True
        thread.flagged = flag
        if commit:
            db.session.commit()
        return True
    except Exception as e:
        if commit:
            db.session.rollback()
        logging.error(f"svc_change_thread_flag was unable to change thread flag. Error: {e}")
        return False

def svc_set_thread_status(thread: MessageThread, new_status: str | ThreadStatus, commit: bool = True) -> bool:
    """
    Will change thread's status. Optionally, commits changes to the DB. Returns True if change was successful, False otherwise.

    :param thread (MessageThread): member of MessageThread model.
    :param new_status (str | ThreadStatus): value or member of ThreadStatus enum.
    :param commit (bool): True if want the changes to be committed to DB (select False if the caller is another service).
    """
    if not thread or not getattr(thread, "id", None):
        logging.error("Invalid or no thread passed to svc_set_thread_status.")
        return False
    
    status = map_string_to_enum(new_status, ThreadStatus)
    if not status:
        logging.error("Invalid status parameter passed to svc_set_thread_status.")
        return False
    try:
        if thread.status == status:
            return True
        thread.status = status
        if commit:
            db.session.commit()
        return True
    except Exception as e:
        if commit:
            db.session.rollback()
        logging.error(f"svc_set_thread_status was unable to change thread status. Error: {e}")
        return False

def svc_set_thread_priority(thread: MessageThread, new_priority: str | ThreadPriority, commit: bool = True) -> bool:
    """
    Will change thread's priority. Optionally, commits changes to the DB. Returns True if change was successful, False otherwise.

    :param thread (MessageThread): member of MessageThread model.
    :param new_priority (str | ThreadPriority): value or member of ThreadPriority enum.
    :param commit (bool): True if want the changes to be committed to DB (select False if the caller is another service).
    """
    if not thread or not getattr(thread, "id", None):
        logging.error("Invalid or no thread passed to svc_set_thread_priority.")
        return False
    
    priority = map_string_to_enum(new_priority, ThreadPriority)
    if not priority:
        logging.error("Invalid priority parameter passed to svc_set_thread_priority.")
        return False
    try:
        if thread.priority == priority:
            return True
        thread.priority = priority
        if commit:
            db.session.commit()
        return True
    except Exception as e:
        if commit:
            db.session.rollback()
        logging.error(f"svc_set_thread_priority was unable to change thread status. Error: {e}")
        return False

def svc_set_thread_category(thread: MessageThread, category: str, commit: bool = True) -> bool:
    """
    Will change thread's category. Optionally, commits changes to the DB. Returns True if change was successful, False otherwise.

    :param thread (MessageThread): member of MessageThread model.
    :param category (str | None): string of maximum 50 chars. Pass None or an empty string to clear it.
    :param commit (bool): True if want the changes to be committed to DB (select False if the caller is another service).
    """
    if not thread or not getattr(thread, "id", None):
        logging.error("Invalid or no thread passed to svc_set_thread_category.")
        return False
    
    if category is not None:
        category = category.strip()

        if len(category) > 50:
            logging.error("Invalid category parameter passed to svc_set_thread_category.")
            return False

        if category == "":
            category = None
    
    try:
        if thread.category == category:
            return True
        thread.category = category
        if commit:
            db.session.commit()
        return True
    except Exception as e:
        if commit:
            db.session.rollback()
        logging.error(f"svc_set_thread_category was unable to change thread category. Error: {e}")
        return False

def svc_assign_thread_to_admin(thread: MessageThread, admin_id: int | None, commit: bool = True) -> bool:
    """
    Will change thread's assigned_to_admin_id. Optionally, commits changes to the DB. Returns True if change was successful, False otherwise.

    :param thread (MessageThread): member of MessageThread model.
    :param admin_id (int | None): id of admin user assigned as responsible for the thread.
    :param commit (bool): True if want the changes to be committed to DB (select False if the caller is another service).
    """
    if not thread or not getattr(thread, "id", None):
        logging.error("Invalid or no thread passed to svc_assign_thread_to_admin.")
        return False
    
    if admin_id is not None and (not isinstance(admin_id, int) or admin_id < 1):
        logging.error("Invalid admin_id parameter passed to svc_assign_thread_to_admin.")
        return False
    try:
        if thread.assigned_to_admin_id == admin_id:
            return True
        thread.assigned_to_admin_id = admin_id
        if commit:
            db.session.commit()
        return True
    except Exception as e:
        if commit:
            db.session.rollback()
        logging.error(f"svc_assign_thread_to_admin was unable to assign admin. Error: {e}")
        return False