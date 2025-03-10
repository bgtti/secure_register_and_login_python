"""
**ABOUT THIS FILE**

seed_logs.py contains the **create_dummie_logs** function, which can be called to create dummie logs in the db for testing and visualization.

Currently used in *seed_all.py* after dummie users are inserted to the db.
"""
import random
from datetime import datetime, timezone
from sqlalchemy import insert
from utils.print_to_terminal import print_to_terminal
from app.extensions.extensions import db, faker
from app.models.user import User
from app.models.log_activity import LogActivity

# Random ips and geolocation chosen from https://www.webpagetest.org/addresses.php
random_ips = ["34.106.208.213", "34.39.131.22", "43.204.105.75", "34.91.238.70", "34.124.137.169", "35.242.177.6", "13.246.114.251", "34.92.96.4", "34.84.123.12", "13.36.154.207"]
ips_and_location = [
    ("34.94.159.140", "Los Angeles, USA"),
    ("34.130.107.20", "Toronto, Canada"),
    ("34.39.131.22", "Sao Paulo, Brazil"),
    ("35.242.177.6", "London, United Kingdom"),
    ("13.36.154.207", "Paris, France"),
    ("34.91.238.70", "Amsterdam, Netherlands"),
    ("13.246.114.251", "Cape Town, South Africa"),
    ("43.204.105.75", "Mumbai, India"),
    ("34.92.96.4", "Hong Kong, China"),
    ("34.84.123.12", "Tokyo, Japan"),
]

# Examples of logging used in the app
logs_examples = [
    ("INFO", 20, "signup","Successful signup.", ""),
    ("INFO", 20, "login", "Successful login.", ""),
    ("INFO", 20, "otp requested", "OTP sent to email.", ""),
    ("INFO", 20, "signup", "Signup failure: user exists.", ""), 
    ("INFO", 20, "password reset token request", "Password reset token sent to email.", ""),
    ("WARNING", 30, "signup", "Signup failed: input does not meet criteria.", "Check if frontend input sanitization failed."), # for user with id 0
    ("SUSPICIOUS", 25, "signup", "Successful signup. Flag assigned.",  faker.text(max_nb_chars=25)),
    ("ERROR", 40, "signup", "Signup failed: could not add user to db.", faker.text(max_nb_chars=80))# for user with id 0
]

def create_log_dic(index, uid, date):
    """
    create_log_dic(index: int, uid:int, date: datetime) -> dict
    ------------------------------------------------------------
    This function will return a dictionary object representing a log.
    Index refers to that of the logs_examples array.
    Used in create_dummie_logs.
    """
    ip_info = random.choice(ips_and_location)
    log = {
            "level":logs_examples[index][0],
            "level_id":logs_examples[index][1],
            "activity": logs_examples[index][2],
            "message": logs_examples[index][3],
            "more_info": logs_examples[index][4],
            "anonymized_ip": ip_info[0],
            "geo_location": ip_info[1],
            "user_agent": faker.user_agent(),
            "user_id": uid,
            "created_at": date,
        }
    return(log)

def create_dummie_logs():
    """
    Creates 52 dummie logs, 50 of which can be linked to a dummie user by id.
    Logs are created and inserted to the LogActivity db.
    Should be used in the create_dummie_user_accts function, after dummie users are created.
    """
    log_list = []
    users = User.query.order_by(User.created_at.desc()).limit(25).all()

    # all users should have signed up and logged in at least once.
    for user in users:
        log_list.extend([create_log_dic(0, user.id, user.created_at), create_log_dic(1, user.id, user.last_seen)])
    
    # some users will have other logs assigned to them
    # Get valid user IDs
    user_ids = [user.id for user in users]
    valid_user_ids = [uid for uid in user_ids if uid != 1]  # Exclude user_id 1 (Super Admin)
    for _ in range(5):
        if user_ids:
            random_user = random.choice(valid_user_ids)
            log_list.extend([
                create_log_dic(2, random_user, datetime.now(timezone.utc)),
                create_log_dic(3, random_user, datetime.now(timezone.utc)),
                create_log_dic(4, random_user, datetime.now(timezone.utc)),
                create_log_dic(6, random_user, datetime.now(timezone.utc)),
            ])

    # some non-registered users may also cause logs
    log_list.extend([
        create_log_dic(5, 0, datetime.now(timezone.utc)),
        create_log_dic(5, 0, datetime.now(timezone.utc)),
        create_log_dic(7, 0, datetime.now(timezone.utc))
    ])

    try:
        db.session.bulk_insert_mappings(LogActivity, log_list)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  
        print_to_terminal(f"Failed to insert dummy logs: {e}", "RED")