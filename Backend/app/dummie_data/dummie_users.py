from datetime import datetime, timedelta
from app.models.user import User
from app.models.stats import UserStats, VisitorStats
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper
from app.utils.console_warning.print_warning import console_warn
from app.extensions import db, flask_bcrypt
from sqlalchemy.orm.session import make_transient
import random
import string
import os
from app.dummie_data.create_files import create_dummie_files

try:
    from app.dummie_data.data_users import user_list
    from app.dummie_data.data_users_stats import user_stats_list
    from app.dummie_data.data_users_visitor_stats import visitor_stats_list
    from app.dummie_data.data_visitor_stats import visitor_stats_random
except ModuleNotFoundError as e:
    console_warn("Creating files for base dummie data.", "CYAN")
    create_dummie_files()

"""
The file named dummie_base_data.py (in this module) created the files data_users.py, data_user_stats.py, data_users_visitor_stats.py, and data_visitor_stats.py.

In this file, we use the data to add dummie input to the database tables at run time.
We adapt these files to the current date in which this app is run to make the data look 'fresh'.

This is used for testing the app and visualize some data in the font end. 
"""

# HELPER FUNCTIONS

def generate_date_obj(num_months_in_the_past, day_of_month=1):
    """
    generate_date_obj(num_months_in_the_past: int, day_of_month:int) -> datetime
    ---------------------------------------------------------------------------
    This function will return a datetime object in the past.

    Parameter: num_months_in_the_past represents the number of months the 
    datetime object should be set in the past. 0 will return the current month,
    1 will return last month, etc.
    day_of_month will set the day of the month for the datetime object.
    ---------------------------------------------------------------------------
    Example usage:
    [if today is the 16th of January 2024]
    date_obj = generate_date_obj(0, 1) -> datetime of the 1st of Jan 2024
    date_obj.month -> January
    """
    # Get the current date
    current_date = datetime.utcnow()

    # Calculate the target month and year
    target_month = current_date.month - num_months_in_the_past
    target_year = current_date.year

    # Adjust the year and month if necessary
    while target_month <= 0:
        target_month += 12
        target_year -= 1

    # Create a datetime object for the target day of the target month
    target_date = datetime(target_year, target_month, day_of_month)

    return target_date

def get_date_obj_week_num(week_num, year):
    """
    get_date_obj_week_num(week_num: int, year: int) -> datetime
    ---------------------------------------------------------------------------
    This function will return a datetime object representing the date of the 
    monday in that week from the specific year.

    Parameter: week_num should be an int between 1 and 52 (53 for 'special' years)
    ---------------------------------------------------------------------------
    Example usage:
    date_obj_1 = get_date_obj_week_num(1, 2024) -> datetime of the 1st of Jan 2024
    date_obj_2 = get_date_obj_week_num(52, 2023) -> datetime of the 4th of December 2024
    date_obj_2.month -> December
    """
    first_day_of_year = datetime(year, 1, 1) # first day of year
    starting_day_of_week = 0  # 0 is Monday, 1 is Tuesday, and so on
    # Calculate the difference between the current day of the week and the starting day
    days_until_start_of_week = (first_day_of_year.weekday() - starting_day_of_week) % 7
    # Subtract the difference to get the first day of the first week of the year
    first_day_of_first_week = first_day_of_year - timedelta(days=days_until_start_of_week)
    # Calculate the difference between the desired week and the first week of the year
    weeks_difference = week_num - first_day_of_year.isocalendar()[1]
    # Calculate the date by adding the difference in weeks to the first day of the first week of the year
    desired_date = first_day_of_first_week + timedelta(weeks=weeks_difference)

    return desired_date

def get_date_obj_last_week():
    """
    get_date_obj_last_week(:void) -> datetime
    ---------------------------------------------------------------------------
    This function will return a datetime object representing the date of last
    week's monday.
    ---------------------------------------------------------------------------
    Example usage:

    [if today is the 16th of January 2024]
    date_obj = get_date_obj_last_week() -> datetime of the 1st of Jan 2024

    [if today is the 2nd of January 2024]
    date_obj_2 = get_date_obj_last_week() -> datetime of the 25th of Dec 2024
    """
    this_year = datetime.now().year
    this_week_num = datetime.date(datetime.utcnow()).isocalendar()[1]
    if this_week_num == 1:
        last_week_of_year = datetime(this_year-1, 12, 31).isocalendar()[1]
        return get_date_obj_week_num(last_week_of_year, this_year-1)
    else: 
        return get_date_obj_week_num(this_week_num-1, this_year)
    
def get_hashed_pw(creation_date, password, salt):
    """
    get_hashed_pw(creation_date: datetime, password: str, salt:str) -> str
    -------------------------------------------------------------------------------------------------------------------
    This function will return a hashed password.
    -------------------------------------------------------------------------------------------------------------------
    Example usage:

    date_today = datetime.now()
    get_hashed_pw(date_today,"hCI969QW", "de53fGnw") -> '$2b$12$zXlbTPBvcwZ/z5uvj3PQ/.fKs7ncxQ62o1gRQQQd.XQunMsPjXaCC'
    """
    pepper = get_pepper(creation_date)
    salted_password = salt + password + pepper
    return flask_bcrypt.generate_password_hash(salted_password).decode('utf-8')


# FAKE DATES
"""
Users are being created for testing purposes and, as such, the date of the account creation is being set accross some dates. Some account creation dates are set to lie 5 months in the past, while others are set with the date of 'today'. To spread them out as evenly as possible, they were separated in time batches defined in NUM_FAKE_USERS_PER_PERIOD. "month_3":15 means to create 15 accounts dated 3 months in the past, spread out accross 5 days in that month (those in FAKE_DAYS_OF_MONTH).

Why are user creation dates being spread out?
To be able to visualize data represented from the Stats module as well (visually represented when logging in the admin dashboard).
"""
TODAY = datetime.utcnow()
YESTERDAY = TODAY - timedelta(days = 1)
THIS_YEAR = datetime.now().year
THIS_MONTH = datetime.now().month
THIS_WEEK_NUM = datetime.date(datetime.utcnow()).isocalendar()[1]

DATE_OBJ_LAST_WEEK = get_date_obj_last_week()
DATE_OBJ_THIS_WEEK = get_date_obj_week_num(THIS_WEEK_NUM, THIS_YEAR)
DATE_OBJ_THIS_MONTH = generate_date_obj(0,1)

FAKE_DAYS_OF_MONTH = [1,5,10,15,25] # month_1 to month_5

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
    # create_dummie_files()
    # Check if Dummy users exist in the database; if not, add them:
    dummies_exist = db.session.query(User).get(2)
    if not dummies_exist:

        console_warn("Adding dummy users to db. This may take a few seconds...", "CYAN")

        index = 0
        the_dates = [] # the_date = (creation_date, the_week, last_seen)

        console_warn("...updating dates in dummie data...", "CYAN")

        for period, num_users in NUM_FAKE_USERS_PER_PERIOD.items():
            if period.startswith("month"):
                num_months_in_the_past = int(period.split("_")[1])
                for i in range(num_users):
                    day_of_month = FAKE_DAYS_OF_MONTH[i % len(FAKE_DAYS_OF_MONTH)]# using the modulo operator (%) to cycle through the values
                    creation_date = generate_date_obj(num_months_in_the_past, day_of_month)
                    the_week = datetime.date(creation_date.year, creation_date.month, creation_date.day).isocalendar()[1]
                    last_seen = YESTERDAY if index % 2 else creation_date # every second user is an active user
                    the_date = (creation_date, the_week, last_seen)

                    the_dates.append(the_date)

                    index += 1

            elif period == "last_week":
                for i in range(num_users):
                    creation_date = get_date_obj_last_week()
                    the_week = datetime.date(creation_date.year, creation_date.month, creation_date.day).isocalendar()[1]
                    last_seen = YESTERDAY if index % 2 else creation_date # every second user is an active user
                    the_date = (creation_date, the_week, last_seen)

                    the_dates.append(the_date)

                    index += 1

            elif period == "this_week":
                for i in range(num_users):
                    creation_date = DATE_OBJ_THIS_WEEK
                    the_week = datetime.date(creation_date.year, creation_date.month, creation_date.day).isocalendar()[1]
                    the_date = (creation_date, the_week, creation_date)

                    the_dates.append(the_date)

                    index += 1

            elif period == "today":
                for i in range(num_users):
                    creation_date = TODAY
                    the_week = datetime.date(creation_date.year, creation_date.month, creation_date.day).isocalendar()[1]
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

        console_warn("...updating dummy data files...", "CYAN")

        file_paths = [
            "data_users.py",
            "data_users_stats.py",
            "data_users_visitor_stats.py",
            "data_visitor_stats.py",
        ]

        data_to_write = [
            (the_data_users, 'user_list'),
            (the_data_users_stats, 'user_stats_list'),
            (the_data_users_visitor_stats, 'visitor_stats_list'),
            (the_data_visitor_stats, 'visitor_stats_random'),
        ]
        
        for i in range(len(file_paths)):
            with open(os.path.join(os.path.dirname(__file__), file_paths[i]), "w", encoding="utf-8") as file:
                if i != 1:
                    file.write(f"from datetime import datetime\n")
                file.write(f"{data_to_write[i][1]} = {data_to_write[i][0]}")

        # dummie_user = User(name=name, email=email, password=hashed_password, salt=salt, created_at=creation_date, last_seen=creation_date)
        # db.session.add_all(dummie_user)
        # db.session.commit()

        # dummie_visitor = VisitorStats(
        #                 ip_address="", 
        #                 continent="",
        #                 country="",
        #                 country_code="",
        #                 city="",
        #                 user_agent = "",
        #                 screen_size= ""
        #                 referrer= ""
        #                 )
        # dummie_user_stats = UserStats(year=creation_date.year, month=creation_date.month, week=the_week, new_user=1, country="")

        # # Make the objects transient to allow them to be added to a new session
        # for user in user_list:
        #     make_transient(user)
        # # Add all users to the session and commit
        # db.session.add_all(user_list)
        # db.session.commit()
        console_warn("...100 dummie users successfully added!", "CYAN")
        print("***************************")
        # users = User.query.all()
        # for user in users:
        #     print(user)