import os
import json
from sqlalchemy import insert
from datetime import datetime, timedelta
from app.extensions import db, flask_bcrypt
from app.models.user import User
from app.models.stats import UserStats, VisitorStats
from app.utils.salt_and_pepper.helpers import get_pepper
from app.utils.console_warning.print_warning import console_warn
from app.dummie_data.create_files import create_dummie_files
from app.dummie_data.dummie_logs import create_dummie_logs

"""
The file named dummie_base_data.py (in this module) created the files data_users.json, data_user_stats.json, data_users_visitor_stats.json, and data_visitor_stats.json.

In this file, we use the data from the .json, make some changes to them, and add them to the database tables when the app is run locally for the first time.
We adapt these files to the current date in which this app is run to make the data look 'fresh'.

This is used for testing the app and visualize some data in the font end. This file should not be used in production.
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

def get_date_from_week_num(week_num, year):
    """
    get_date_from_week_num(week_num: int, year: int) -> datetime
    ---------------------------------------------------------------------------
    This function will return a datetime object representing the date of the 
    monday in that week from the specific year.

    Parameter: week_num should be an int between 1 and 52 (53 for 'special' years)
    ---------------------------------------------------------------------------
    Example usage:
    date_obj_1 = get_date_from_week_num(1, 2024) -> datetime of the 1st of Jan 2024
    date_obj_2 = get_date_from_week_num(52, 2023) -> datetime of the 4th of December 2024
    date_obj_2.month -> December
    """
    if week_num < 10:
        string_date = f"{year}-0{week_num}-"
    else:
        string_date = f"{year}-{week_num}-"
    date = datetime.strptime(string_date + "1", "%Y-%W-%w") # 1 & %w tells parser to pick the monday in that week

    return date

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
        return get_date_from_week_num(last_week_of_year, this_year-1)
    else: 
        return get_date_from_week_num(this_week_num-1, this_year)
    
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
THIS_WEEK_NUM = datetime.date(datetime.utcnow()).isocalendar()[1]

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
    # Check if Dummy users exist in the database; if not, add them:
    dummies_exist = db.session.query(User).get(2)

    if not dummies_exist:

        file_names = [
            "data_users.json",
            "data_users_stats.json",
            "data_users_visitor_stats.json",
            "data_visitor_stats.json",
        ]
        data_lists = []

        # Check if any file is not found
        if any(not os.path.exists(f"app/dummie_data/{file_name}") for file_name in file_names):
            console_warn("Creating files for base dummy data.", "CYAN")
            create_dummie_files()

        # Load data from all files
        for file_name in file_names:
            with open(os.path.join(os.path.dirname(__file__), file_name), "r", encoding="utf-8") as file:
                data = json.load(file)

            data_lists.append(data)

        user_list, user_stats_list, visitor_stats_list, visitor_stats_random = data_lists

        console_warn("Adding dummy users to db. This may take a few seconds...", "CYAN")

        index = 0
        the_dates = [] # the_date = (creation_date, the_week, last_seen)

        console_warn("...updating dates in dummie data...", "CYAN")

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
        
        console_warn("...adding dummie users to db...", "CYAN")
        db.session.execute(insert(User), the_data_users)

        console_warn("...adding dummie users to stats db...", "CYAN")
        db.session.execute(insert(UserStats), the_data_users_stats)

        console_warn("...adding some more dummie stats to db...", "CYAN")
        db.session.execute(insert(VisitorStats), the_data_users_visitor_stats)
        db.session.execute(insert(VisitorStats), the_data_visitor_stats)

        db.session.commit()

        console_warn("...adding some dummie logs to db...", "CYAN")
        create_dummie_logs()

        console_warn("100 users created successfully!", "CYAN")
        print()
        console_warn("Happy coding!", "GREEN")
        print()

        # Uncomment bellow to debug:
        # users = User.query.all()
        # for user in users:
        #     print(user)

        # ***** UPDATING THE JSON:
        # There are two possible approaches for inserting in bulk to the DB. One is inserting from memory, and the other would be saving the data to the json file and then adding to the db from the json file. This code is using the first approach, so the json files won't be updated with the changes made here.
        # If you want to update the json files to visualize the changes made to them, you can uncomment the code bellow:

        # # Custom JSON encoder to handle datetime serialization
        # # This should avoid TypeError: Object of type datetime is not JSON serializable
        # console_warn("...updating dummy data files...", "CYAN")
        # class DateTimeEncoder(json.JSONEncoder):
        #     def default(self, obj):
        #         if isinstance(obj, datetime):
        #             return obj.isoformat()
        #         return super().default(obj)

        # data_to_write = [
        #     the_data_users,
        #     the_data_users_stats,
        #     the_data_users_visitor_stats,
        #     the_data_visitor_stats
        # ]

        # for i in range(len(file_names)):
        #     with open(os.path.join(os.path.dirname(__file__), file_names[i]), "w", encoding="utf-8") as file:
        #         json.dump(data_to_write[i], file, indent=4, cls=DateTimeEncoder)  # Use json.dump to write the data as JSON

        



# *** USING .PY INSTEAD OF .JSON
# The function above used to get data from .py files, and re-write it there.
# Json is more human-readable and in most cases the recommended way to work with data.
# Still, in case you want to use .py files instead of json, these are the relevant parts of the old code:
# [importing the files: using # type: ignore at the end so VS code would not add it as a problem when the module wasn't found:]
#         try:
#             from app.dummie_data.data_users import user_list  # type: ignore
#             from app.dummie_data.data_users_stats import user_stats_list  # type: ignore
#             from app.dummie_data.data_users_visitor_stats import visitor_stats_list  # type: ignore
#             from app.dummie_data.data_visitor_stats import visitor_stats_random  # type: ignore
#         except ModuleNotFoundError as e:
#             console_warn("Creating files for base dummie data.", "CYAN")
#             create_dummie_files()
        
#         from app.dummie_data.data_users import user_list  # type: ignore
#         from app.dummie_data.data_users_stats import user_stats_list  # type: ignore
#         from app.dummie_data.data_users_visitor_stats import visitor_stats_list  # type: ignore
#         from app.dummie_data.data_visitor_stats import visitor_stats_random  # type: ignore
#
# [writing to files:]
# file_paths = [
        #     "data_users.py",
        #     "data_users_stats.py",
        #     "data_users_visitor_stats.py",
        #     "data_visitor_stats.py",
        # ]
        
        # data_to_write = [
        #     (the_data_users, 'user_list'),
        #     (the_data_users_stats, 'user_stats_list'),
        #     (the_data_users_visitor_stats, 'visitor_stats_list'),
        #     (the_data_visitor_stats, 'visitor_stats_random'),
        # ]
        # for i in range(len(file_paths)):
        #     with open(os.path.join(os.path.dirname(__file__), file_paths[i]), "w", encoding="utf-8") as file:
        #         if i != 1:
        #             file.write(f"import datetime\n")
        #         file.write(f"{data_to_write[i][1]} = {data_to_write[i][0]}")