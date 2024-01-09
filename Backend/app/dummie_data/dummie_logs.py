from sqlalchemy import insert
from app.extensions import db
from datetime import datetime
from app.models.user import User
from app.models.log_event import LogEvent

"""
This file contains the create_dummie_logs function, which can be called to create dummie logs in the db for testing and visualization.
Currently used in dummie_users.py after dummie users are inserted to the db.
"""

logs_examples = [
    ("INFO", "signup","successful signup.", 20),
    ("INFO", "login", "successful login.", 20),
    ("WARN", "signup", "signup failure: user could not be created.", 40),
    ("WARN", "signup", "signup rejected: weak password. Frontend validation failed?", 20)
]

def create_log_dic(index, uuid, date):
    """
    create_log_dic(index: int, uuid:str, date: datetime) -> dict
    ------------------------------------------------------------
    This function will return a dictionary object representing a log.
    Index refers to that of the logs_examples array.
    Used in create_dummie_logs.
    """
    log = {
            "_level":logs_examples[index][3],
            "_type": logs_examples[index][0],
            "_activity": logs_examples[index][1],
            "_message": logs_examples[index][2],
            "_user_uuid": uuid,
            "_created_at": date,
        }
    return(log)

def create_dummie_logs():
    """
    Creates 52 dummie logs, 50 of which can be linked to a dummie user by uuid.
    Logs are created and inserted to the LogEvent db.
    Should be used in the create_dummie_user_accts function, after dummir users are created.
    """
    log_list = []
    users = User.query.order_by(User._created_at.desc()).limit(25).all()
    for user in users:
        log_list.extend([create_log_dic(0, user.uuid, user.created_at), create_log_dic(1, user.uuid, user.last_seen)])
    log_list.extend([
        create_log_dic(2, "", datetime.utcnow()),
        create_log_dic(3, "", datetime.utcnow())
    ])

    db.session.execute(insert(LogEvent), log_list)
    db.session.commit()

