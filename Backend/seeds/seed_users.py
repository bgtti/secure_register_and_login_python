"""
**ABOUT THIS FILE**

In seed_users.py we use the data from the json files (inside the *files* directory) to add users to the database tables when the app runs locally for the first time. The date stamps are adapted in accordance to the current date in which this app is run to make the data look 'fresh'.

The json files herein mentioned were created by *create_seed_files.py* (in the seeds package). They are: data_users.json, data_user_stats.json, data_users_visitor_stats.json, and data_visitor_stats.json.
"""
import os
import json
from datetime import datetime, timedelta, timezone
from sqlalchemy import insert
from utils.print_to_terminal import print_to_terminal
from seeds.files.create_seed_files import SEED_FILES_JSON
from seeds.helpers import generate_date_obj, get_date_from_week_num, get_date_obj_last_week, get_hashed_pw
from app.extensions import db
from app.models.user import User
from app.models.stats import UserStats, VisitorStats

# FAKE DATES
"""
**About fake dates**

Users are being created for testing purposes and, as such, the date of the account creation is being set accross some dates. Some account creation dates are set to lie 5 months in the past, while others are set with the date of 'today'. To spread them out as evenly as possible, they were separated in time batches defined in NUM_FAKE_USERS_PER_PERIOD. "month_3":15 means to create 15 accounts dated 3 months in the past, spread out accross 5 days in that month (those in FAKE_DAYS_OF_MONTH).

Why are user creation dates being spread out?
To be able to visualize data represented from the Stats module as well (visually represented when logging in the admin dashboard).
"""

TODAY = datetime.now(timezone.utc)
YESTERDAY = TODAY - timedelta(days = 1)
THIS_YEAR = datetime.now().year
THIS_WEEK_NUM = datetime.date(datetime.now(timezone.utc)).isocalendar()[1]

DATE_OBJ_LAST_WEEK = get_date_obj_last_week()
DATE_OBJ_THIS_WEEK = get_date_from_week_num(THIS_WEEK_NUM, THIS_YEAR)
DATE_OBJ_THIS_MONTH = generate_date_obj(0,1)

FAKE_DAYS_OF_MONTH = [1,5,10,15,25] # month_1 to month_3. Only used in month_0 if TODAY.day > 25.

NUM_FAKE_USERS_PER_PERIOD = {
    "month_3":10,# creation_date -> generate_date_obj(num_months_in_the_past, day_of_month) where num_months_in_the_past is 3 and day_of_month is FAKE_DAYS_OF_MONTH
    "month_2":20,# creation_date -> generate_date_obj(num_months_in_the_past, day_of_month) where num_months_in_the_past is 3 and day_of_month is FAKE_DAYS_OF_MONTH
    "month_1":25,# creation_date -> generate_date_obj(num_months_in_the_past, day_of_month) where num_months_in_the_past is 2 and day_of_month is FAKE_DAYS_OF_MONTH
    "month_0":15, # creation_date = DATE_OBJ_THIS_MONTH --->this month
    "last_week":10, # creation_date = DATE_OBJ_LAST_WEEK
    "this_week":15, # creation_date = DATE_OBJ_THIS_WEEK
    "today":5, # creation_date = TODAY
}

def create_dummie_user_accts():
    """
    Creates 100 dummy users in the db for testing purposes.
    This function is called in manage.py (dev environment only).
    """
    data_lists = []

    # Load data from all files
    for file_name in SEED_FILES_JSON:
        file_path = os.path.join(os.path.dirname(__file__), f'files/{file_name}')
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        data_lists.append(data)
    user_list, user_stats_list, visitor_stats_list, visitor_stats_random = data_lists

    index = 0
    the_dates = [] # the_date = (creation_date, the_week, last_seen)

    print_to_terminal("...updating dates in dummie data...", "CYAN")

    for period, num_users in NUM_FAKE_USERS_PER_PERIOD.items():
        if period.startswith("month"):
            num_months_in_the_past = int(period.split("_")[1])
            for i in range(num_users):
                if period == "month_0" and TODAY.day < 25: 
                    creation_date = DATE_OBJ_THIS_MONTH
                else:
                    day_of_month = FAKE_DAYS_OF_MONTH[i % len(FAKE_DAYS_OF_MONTH)]# using the modulo operator (%) to cycle through the values
                    creation_date = generate_date_obj(num_months_in_the_past, day_of_month)
                the_week = datetime.date(creation_date).isocalendar()[1]
                last_seen = YESTERDAY if index % 2 else creation_date # every second user is an active user
                the_date = (creation_date, the_week, last_seen)
                the_dates.append(the_date)
                index += 1
        elif period == "last_week":
            for i in range(num_users):
                creation_date = DATE_OBJ_LAST_WEEK
                the_week = datetime.date(creation_date).isocalendar()[1]
                last_seen = YESTERDAY if index % 2 else creation_date # every second user is an active user
                the_date = (creation_date, the_week, last_seen)
                the_dates.append(the_date)
                index += 1
        elif period == "this_week":
            for i in range(num_users):
                creation_date = DATE_OBJ_THIS_WEEK
                the_week = datetime.date(creation_date).isocalendar()[1]
                the_date = (creation_date, the_week, creation_date)
                the_dates.append(the_date)
                index += 1
        elif period == "today":
            for i in range(num_users):
                creation_date = TODAY
                the_week = THIS_WEEK_NUM
                the_date = (creation_date, the_week, creation_date)
                the_dates.append(the_date)
                index += 1
    
    the_data_users = []
    the_data_users_stats = []
    the_data_users_visitor_stats = []
    the_data_visitor_stats = []
    for i in range(len(user_list)):
        user = user_list[i]
        user['password'] = get_hashed_pw(creation_date, user['password'], user['salt'])
        user['created_at'] = the_dates[i][0]
        user['last_seen'] = the_dates[i][2]
        the_data_users.append(user)
    for i in range(len(user_stats_list)):
        user_stats = user_stats_list[i]
        user_stats['year'] = the_dates[i][0].year
        user_stats['month'] = the_dates[i][0].month
        user_stats['week'] = the_dates[i][1]
        the_data_users_stats.append(user_stats)
    
    index_j = 0
    for i in range(len(the_dates)):
        date = the_date = the_dates[i][0]
        for j in range(index_j, index_j+2):
            visitor_user_stats = visitor_stats_list[j]
            visitor_user_stats['date_accessed'] = date
            the_data_users_visitor_stats.append(visitor_user_stats)
            visitor_random = visitor_stats_random[j]
            visitor_random['date_accessed'] = date
            the_data_visitor_stats.append(visitor_random)
            
        index_j += 2
    # with executing bulk addition to the db, the __init__ db method is skipped.
    # execute with insert bypasses the ORM layer's object creation
    # this means the original table values have to be used instead of the defined @property
    # example: "_name" must be used instead of "name" to be inserted into the User model directly.
    
    print_to_terminal("...seeding the db with users...", "CYAN")
    db.session.execute(insert(User), the_data_users)
    print_to_terminal("...seeding the db with stats...", "CYAN")
    db.session.execute(insert(UserStats), the_data_users_stats)
    db.session.execute(insert(VisitorStats), the_data_users_visitor_stats)
    db.session.execute(insert(VisitorStats), the_data_visitor_stats)
    db.session.commit()

    # Uncomment bellow to debug:
    # users = User.query.all()
    # for user in users:
    #     print(user)


    # ***** UPDATING THE JSON:
    # There are two possible approaches for inserting in bulk to the DB. One is inserting from memory, and the other would be saving the data to the json file and then adding to the db from the json file. This code is using the first approach, so the json files won't be updated with the changes made here.
