"""
**ABOUT THIS FILE**

seed_logs.py contains the **create_dummie_logs** function, which can be called to create dummie logs in the db for testing and visualization.

Currently used in *seed_all.py* after dummie users are inserted to the db.
"""
from datetime import datetime, timezone
from sqlalchemy import insert
from app.extensions import db
from app.models.user import User
from app.models.log_event import LogEvent

logs_examples = [
    ("INFO", "signup","successful signup.", 20),
    ("INFO", "login", "successful login.", 20),
    ("WARN", "signup", "signup failure: user could not be created.", 40),
    ("WARN", "signup", "signup rejected: weak password. Frontend validation failed?", 20)
]

def create_log_dic(index, uid, date):
    """
    create_log_dic(index: int, uid:int, date: datetime) -> dict
    ------------------------------------------------------------
    This function will return a dictionary object representing a log.
    Index refers to that of the logs_examples array.
    Used in create_dummie_logs.
    """
    log = {
            "level":logs_examples[index][3],
            "type": logs_examples[index][0],
            "activity": logs_examples[index][1],
            "message": logs_examples[index][2],
            "user_id": uid,
            "created_at": date,
        }
    return(log)

def create_dummie_logs():
    """
    Creates 52 dummie logs, 50 of which can be linked to a dummie user by uuid.
    Logs are created and inserted to the LogEvent db.
    Should be used in the create_dummie_user_accts function, after dummir users are created.
    """
    log_list = []
    users = User.query.order_by(User.created_at.desc()).limit(25).all()
    for user in users:
        log_list.extend([create_log_dic(0, user.id, user.created_at), create_log_dic(1, user.id, user.last_seen)])
    log_list.extend([
        create_log_dic(2, 0, datetime.now(timezone.utc)),
        create_log_dic(3, 0, datetime.now(timezone.utc))
    ])

    db.session.execute(insert(LogEvent), log_list)
    db.session.commit()