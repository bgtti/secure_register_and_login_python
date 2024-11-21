"""
**ABOUT THIS FILE**

seeds/helpers.py contains helper functions that are used in files throughout the seeds package.

The following functions deal with with date handling:
- **generate_date_obj**, 
- **get_date_from_week_num**, 
- **get_date_obj_last_week**

**get_hashed_pw** spits out a hashed password
**generate_fake_mail** returns a fake email address given a name

"""
from datetime import datetime, timezone
from app.extensions.extensions import flask_bcrypt
from app.utils.salt_and_pepper.helpers import get_pepper

# DATE-RELATED FUNCTIONS

def generate_date_obj(num_months_in_the_past, day_of_month=1):
    """
    generate_date_obj(num_months_in_the_past: int, day_of_month:int) -> datetime
    ---------------------------------------------------------------------------

    This function will return a datetime object in the past.
    *Arguments*: 
    - num_months_in_the_past represents the number of months the datetime object should be set in the past. 0 will return the current month, 1 will return last month, etc.
    - day_of_month will set the day of the month for the datetime object.

    ---------------------------------------------------------------------------
    Example usage:

    #*if today is the 16th of January 2024:*

    `date_obj = generate_date_obj(0, 1) #-> datetime of the 1st of Jan 2024`

    `date_obj.month #-> January`
    """
    # Get the current date
    current_date = datetime.now(timezone.utc)

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

    **Arguments**: 
    - week_num should be an int between 1 and 52 (53 for 'special' years)
    - year is the int representing the desired year
    ---------------------------------------------------------------------------
    Example usage:

    `date_obj_1 = get_date_from_week_num(1, 2024) #-> datetime of the 1st of Jan 2024`

    `date_obj_2 = get_date_from_week_num(52, 2023) #-> datetime of the 4th of December 2024`

    `date_obj_2.month #-> December`
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

    *# if today is the 16th of January 2024:*
    `date_obj = get_date_obj_last_week() #-> datetime of the 1st of Jan 2024`

    *# if today is the 2nd of January 2024:*
    `date_obj_2 = get_date_obj_last_week() #-> datetime of the 25th of Dec 2024`
    """
    this_year = datetime.now().year
    this_week_num = datetime.date(datetime.now(timezone.utc)).isocalendar()[1] 
    if this_week_num == 1:
        last_week_of_year = datetime(this_year-1, 12, 31).isocalendar()[1]
        return get_date_from_week_num(last_week_of_year, this_year-1)
    else: 
        return get_date_from_week_num(this_week_num-1, this_year)
    
# PASSWORD-RELATED FUNCTION

def get_hashed_pw(creation_date, password, salt):
    """
    get_hashed_pw(creation_date: datetime, password: str, salt:str) -> str
    ----------------------------------------------------------------------

    Given a date, password, and salt, this function will return the hashed password.

    ----------------------------------------------------------------------
    Example usage:

    `date_today = datetime.now()`

    `get_hashed_pw(date_today,"hCI969QW", "de53fGnw") #-> '$2b$12$zXlbTPBvcwZ/z5uvj3PQ/.fKs7ncxQ62o1gRQQQd.XQunMsPjXaCC'`
    """
    pepper = get_pepper(creation_date)
    salted_password = salt + password + pepper
    return flask_bcrypt.generate_password_hash(salted_password).decode('utf-8')

# EMAIL-RELATED FUNCTION
def generate_fake_mail(name):
    """
    generate_fake_mail(name: str) -> str
    ---------------------------------------------------------------------------

    This function takes a name, removes special characters, put it in lowercase,
    joins first/middle/last names with a . and suffixed it with @fakemail.com

    ---------------------------------------------------------------------------
    Example usage:
    
    `generate_fake_mail("David") # -> david@fakemail.com`

    `generate_fake_mail("Charles Szabó") # -> charles.szabo@fakemail.com`

    `generate_fake_mail("João Martinez de Sá Peixoto") # -> joao.martinez.de.sa.peixoto@fakemail.com`
    """
    cleaned_name = "".join(c.lower() if c.isalnum() or c.isspace() else "." for c in name)
    cleaned_name = " ".join(cleaned_name.split()) # Replace consecutive spaces with a single space
    cleaned_name = cleaned_name.replace(" ", ".") # Replace spaces with dots
    fake_email = f"{cleaned_name}@fakemail.com"
    return fake_email