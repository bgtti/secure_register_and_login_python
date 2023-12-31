from datetime import datetime, timedelta
from app.models.user import User
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper
from app.utils.console_warning.print_warning import console_warn
from app.extensions import db, flask_bcrypt
import random
import string

# DUMMIE NAMES
DUMMIES = ["James Maung", "Mary Zhu", "Robert Lu", "Patricia Khan", "Dorothy", "James Ali", "Mary Kumar", "Robert Singh", "Patricia Devi", "John Zhang", "Jennifer Wang", "Michael dos Santos", "Linda Schmidt", "David Schneider", "Elizabeth Becker", "William Bauer", "Barbara Dubois", "Richard Leroy", "Susan Bruno", "Joseph Ricci", "Jessica Marino", "Thomas Colombo", "Sarah Ferrari", "Jason", "Christopher Bianchi", "Karen Nagy", "Charles Szabó", "Lisa Kovács", "Daniel Jansen", "Nancy Viser", "Matthew Vanderberg", "Betty Almeida", "Anthony Oliveira", "Sandra Carvalho", "Mark Oni", "Melissa", "Margaret Taiwo", "Donald Zabu", "Ashley Simpson", "Steven Tyjani", "Kimberly Smit", "Andrew Badenhorst", "Emily Nel", "Paul van der Merwe", "Donna Asrat", "Joshua Tamesgen", "Michelle Ibrahim", "Kenneth Hassan", "Carol Akil", "Kevin Adel", "Amanda Ahmad", "George", "Brian Abdallah", "Deborah", "Anna Scott", "Nicole Roberts", "Brandon Carter", "Samantha Mitchell", "Brenda", "Benjamin Campbell", "Katherine Rivera", "Shirley", "Samuel Hall", "Christine Baker", "Gregory Nelson", "Helen Adams", "Alexander Green", "Debra Flores", "Patrick Hill", "Rachel Nguyen", "Frank Torres", "Carolyn Scott", "Stephanie O", "Nicholas", "Peter Hernandez", "Raymond Wright", "Janet King", "Jack Allen", "Maria Young", "Dennis Walker", "Kyle Rodriguez", "Catherine Robinson", "Jerry Lewis", "Heather Ramirez", "Tyler Clark", "Diane Sanchez", "Aaron Harris", "Olivia White", "Jose Thompson", "Julie Perez", "Adam Lee", "Joyce Martin", "Nathan Jackson", "Timothy", "Victoria Moore", "Henry Taylor", "Ruth Thomas", "Zachary Anderson", "Virginia Wilson", "Douglas Gonzalez", "Lauren Lopez", "Kelly Martinez", "Christina Davis", "Noah Garcia", "Joan Miller", "Ethan Jones", "Evelyn Brown", "Jeremy Williams", "Judith Johnson", "Walter Smith"]

# # --- 2. Instantiate an instance of faker:
# fake = Faker(locale = "en_GB")

# install faker: https://towardsdatascience.com/how-to-create-fake-data-with-faker-a835e5b7a9d9
# DUMMIE_ANALYTICS_DATA = [ --> generate with faker https://faker.readthedocs.io/en/master/
#     {
#     "ip_address": "...",
#     "continent": "...",
#     "country": "...",
#     "country_code": "...",
#     "city": "...",
#     "user_agent": "...",
#     "os": "...",
#     "screen_size": "( 0x0 )",
#     "referrer": "...",
#     "page_accessed": "...",
#     "session_visit": "...",
#     }
# ]

DUMMY_PLACES = [
    ("Africa", "Egypt", "EG", "Cairo"),
    ("Africa", "Nigeria", "NG", "Lagos"),
    ("Africa", "South Africa", "ZA", "Cape Town"),
    ("Africa", "South Africa", "ZA", "Durban"),
    ("Africa", "South Africa", "ZA", "Johannesburg"),
    ("Asia", "India", "IN", "Mumbai"),
    ("Asia", "India", "IN", "Jaipur"),
    ("Asia", "Indonesia", "ID", "Jakarta"),
    ("Asia", "Japan", "JP", "Tokio"),
    ("Asia", "Japan", "JP", "Yokohama"),
    ("Asia", "Japan", "JP", "Osaka"),
    ("Europe", "France", "FR", "Paris"),
    ("Europe", "France", "FR", "Toulouse"),
    ("Europe", "France", "FR", "Marseille"),
    ("Europe", "Hungary", "HU", "Budapest"),
    ("Europe", "Ireland", "IE", "Dublin"),
    ("Europe", "Italy", "IT", "Milan"),
    ("Europe", "Italy", "IT", "Rome"),
    ("Europe", "Germany", "DE", "Berlin"),
    ("Europe", "Germany", "DE", "Munich"),
    ("Europe", "Germany", "DE", "Frankfurt"),
    ("Europe", "Germany", "DE", "Hamburg"),
    ("Europe", "Germany", "DE", "Cologne"),
    ("Europe", "Netherlands", "NL", "Amsterdam"),
    ("Europe", "Netherlands", "NL", "Rotterdam"),
    ("Europe", "Spain", "ES", "Barcelona"),
    ("Europe", "Spain", "ES", "Madrid"),
    ("Europe", "Spain", "ES", "Valencia"),
    ("Europe", "Portugal", "PT", "Lisbon"),
    ("Europe", "Portugal", "PT", "Porto"),
    ("Europe", "United Kingdom", "GB","London"),
    ("Europe", "United Kingdom", "GB","Liverpool"),
    ("Europe", "United Kingdom", "GB","Bristol"),
    ("Europe", "United Kingdom", "GB","Belfast"),
    ("Europe", "United Kingdom", "GB","Leeds"),
    ("Europe", "United Kingdom", "GB","Glasgow"),
    ("North America", "Mexico", "MX","Mexico City"),
    ("North America", "USA", "US","New York"),
    ("North America", "USA", "US","San Francisco"),
    ("North America", "USA", "US","Austin"),
    ("North America", "USA", "US","Los Angeles"),
    ("North America", "USA", "US","Chicago"),
    ("North America", "USA", "US","Seattle"),
    ("North America", "USA", "US","Portland"),
    ("North America", "USA", "US","Denver"),
    ("South America", "Brazil", "BR","Sao Paulo"),
    ("South America", "Brazil", "BR","Rio de Janeiro"),
    ("South America", "Brazil", "BR","Fortaleza"),
    ("South America", "Chile", "CL","Valparaiso"),
    ("South America", "Colombia", "CO","Bogota"),
    ("South America", "Uruguay", "UY","Montevideo"),
    ("Oceania", "Australia", "AU","Sydney"),
    ("Oceania", "Australia", "AU","Melbourne"),
]


# DUMMY_ANALYTICS_DATA = [
#     {
#         "ip_address": fake.ipv4(),
#         "continent": fake.random_element(elements=("Asia", "Europe", "North America", "South America", "Africa", "Australia")),
#         "country": fake.country(),
#         "country_code": fake.country_code(),
#         "city": fake.city(),
#     },
#     {
#         ....
#     }
# ]


# def create_localized_faker ():
#     # US
#     Faker.seed(0)
#     for _ in range(5):
#         fake.city()
#         fake.country()
#         fake.country_code()


# HELPER FUNCTIONS
def generate_fake_mail(name):
    """
    generate_fake_mail(name: str) -> str
    ---------------------------------------------------------------------------
    This function takes a name, removes special characters, put it in lowercase,
    joins first/middle/last names with a . and suffixed it with @fakemail.com
    ---------------------------------------------------------------------------
    Example usage:
    
    generate_fake_mail("David") -> david@fakemail.com
    generate_fake_mail("Charles Szabó") -> charles.szabo@fakemail.com
    generate_fake_mail("João Martinez de Sá Peixoto") -> joao.martinez.de.sa.peixoto@fakemail.com
    """
    cleaned_name = "".join(c.lower() if c.isalnum() or c.isspace() else "." for c in name)
    cleaned_name = " ".join(cleaned_name.split()) # Replace consecutive spaces with a single space
    cleaned_name = cleaned_name.replace(" ", ".") # Replace spaces with dots
    fake_email = f"{cleaned_name}@fakemail.com"
    return fake_email

def generate_fake_str():
    """
    generate_fake_str(:void) -> str
    ---------------------------------------------------------------------------
    This function takes no arguments and returns a random 8-character string
    ---------------------------------------------------------------------------
    Example usage:
    [if today is the 16th of January 2024]
    date_obj = generateDateObjt(0, 1) -> datetime of the 1st of Jan 2024
    date_obj.month -> January
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

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


# FAKE DATES
"""
Users are being created for testing purposes and, as such, the date of the account creation is being set accross some dates. Some account creation dates are set to lie 5 months in the past, while others are set with the date of 'today'. To spread them out as evenly as possible, they were separated in time batches defined in NUM_FAKE_USERS_PER_PERIOD. "month_3":15 means to create 15 accounts dated 3 months in the past, spread out accross 5 days in that month (those in FAKE_DAYS_OF_MONTH).

Why are user creation dates being spread out?
To be able to visualize data represented from the Stats module as well (visually represented when logging in the admin dashboard).
"""
TODAY = datetime.utcnow()
THIS_YEAR = datetime.now().year
THIS_MONTH = datetime.now().month
THIS_WEEK_NUM = datetime.date(datetime.utcnow()).isocalendar()[1]

DATE_OBJ_LAST_WEEK = get_date_obj_last_week()
DATE_OBJ_THIS_WEEK = get_date_obj_week_num(THIS_WEEK_NUM, THIS_YEAR)
DATE_OBJ_THIS_MONTH = generate_date_obj(0,1)

FAKE_DAYS_OF_MONTH = [1,5,10,15,25] # month_1 to month_5

NUM_FAKE_USERS_PER_PERIOD = {
    "month_5":5, # creation_date -> generate_date_obj(num_months_in_the_past, day_of_month) where num_months_in_the_past is 5 and day_of_month is FAKE_DAYS_OF_MONTH
    "month_4":10, # creation_date -> generate_date_obj(num_months_in_the_past, day_of_month) where num_months_in_the_past is 4 and day_of_month is FAKE_DAYS_OF_MONTH
    "month_3":15,# creation_date -> generate_date_obj(num_months_in_the_past, day_of_month) where num_months_in_the_past is 3 and day_of_month is FAKE_DAYS_OF_MONTH
    "month_2":20,# creation_date -> generate_date_obj(num_months_in_the_past, day_of_month) where num_months_in_the_past is 3 and day_of_month is FAKE_DAYS_OF_MONTH
    "month_1":25,# creation_date -> generate_date_obj(num_months_in_the_past, day_of_month) where num_months_in_the_past is 2 and day_of_month is FAKE_DAYS_OF_MONTH
    "this_month":15, # creation_date = DATE_OBJ_THIS_MONTH
    "last_week":5, # creation_date = DATE_OBJ_LAST_WEEK
    "this_week":10, # creation_date = DATE_OBJ_THIS_WEEK
    "today":5, # creation_date = TODAY
}

# CREATING DUMMIE USERS

def create_dummie_user_accts():
    """
    Creates 110 dummie users in the db for testing purposes.
    This function is called in manage.py (dev environment only).
    """
    # Check if Dummie users exists in the database, if not, add it:
    dummies_exist = db.session.query(User).get(2)
    if not dummies_exist:
        console_warn("Adding dummie users to db. This may take a few seconds...", "CYAN")
        index = 0
        for period, num_users in NUM_FAKE_USERS_PER_PERIOD.items(): #.items() returns tuples: [("month_5", 5), ("month_4", 10), ...]
            if period.startswith("month"):
                num_months_in_the_past = int(period.split("_")[1])
                for i in range(num_users):
                    day_of_month = FAKE_DAYS_OF_MONTH[i % len(FAKE_DAYS_OF_MONTH)] # using the modulo operator (%) to cycle through the values
                    creation_date = generate_date_obj(num_months_in_the_past, day_of_month)
                    name = DUMMIES[index]
                    email = generate_fake_mail(name)
                    password = generate_fake_str()
                    salt = generate_fake_str()
                    pepper = get_pepper(creation_date)
                    salted_password = salt + password + pepper
                    hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode('utf-8')
                    dummie_user = User(name=name, email=email, password=hashed_password, salt=salt, created_at=creation_date, last_seen=creation_date)
                    db.session.add(dummie_user)
                    index += 1
            elif period == "this_month":
                for i in range(num_users):
                    creation_date = DATE_OBJ_THIS_MONTH
                    name = DUMMIES[index]
                    email = generate_fake_mail(name)
                    password = generate_fake_str()
                    salt = generate_fake_str()
                    pepper = get_pepper(creation_date)
                    salted_password = salt + password + pepper
                    hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode('utf-8')
                    dummie_user = User(name=name, email=email, password=hashed_password, salt=salt, created_at=creation_date, last_seen=creation_date)
                    db.session.add(dummie_user)
                    index += 1
            elif period == "last_week":
                for i in range(num_users):
                    creation_date = DATE_OBJ_LAST_WEEK
                    name = DUMMIES[index]
                    email = generate_fake_mail(name)
                    password = generate_fake_str()
                    salt = generate_fake_str()
                    pepper = get_pepper(creation_date)
                    salted_password = salt + password + pepper
                    hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode('utf-8')
                    dummie_user = User(name=name, email=email, password=hashed_password, salt=salt, created_at=creation_date, last_seen=creation_date)
                    db.session.add(dummie_user)
                    index += 1
            elif period == "this_week":
                for i in range(num_users):
                    creation_date = DATE_OBJ_THIS_WEEK
                    name = DUMMIES[index]
                    email = generate_fake_mail(name)
                    password = generate_fake_str()
                    salt = generate_fake_str()
                    pepper = get_pepper(creation_date)
                    salted_password = salt + password + pepper
                    hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode('utf-8')
                    dummie_user = User(name=name, email=email, password=hashed_password, salt=salt, created_at=creation_date, last_seen=creation_date)
                    db.session.add(dummie_user)
                    index += 1
            elif period == "today":
                for i in range(num_users):
                    creation_date = TODAY
                    name = DUMMIES[index]
                    email = generate_fake_mail(name)
                    password = generate_fake_str()
                    salt = generate_fake_str()
                    pepper = get_pepper(creation_date)
                    salted_password = salt + password + pepper
                    hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode('utf-8')
                    dummie_user = User(name=name, email=email, password=hashed_password, salt=salt, created_at=creation_date, last_seen=creation_date)
                    db.session.add(dummie_user)
                    index += 1
        db.session.commit()
        console_warn("...110 dummie users successfully added!", "CYAN")
        # uncomment the bellow to print all users created:
        # users = User.query.all()
        # for user in users:
        #     print(user)

# def set_last_seen():
#     INDEXES = [1,3,4,]


# FUNCTION THAT CREATES ALL DUMMIE DATA
# def create_dummie_data():
#     create_dummie_user_accts()



# create_dummie_user_accts()

# {
#         "name": "", 
#         "email": "",
#         "password": "",
#         "salt": "", 
#     }



# Some dummie data will populate the db of the dev envinroment for testing purposes
# The datetime stamps were faked for this purpose
# All user accounts are created in the span of 6 months


# def create_dummie_stats():
#     """
#     Creates fake stats in the db for testing purposes.
#     This function is called in manage.py (dev environment only).
#     """
#     this_year = datetime.now().year
#     this_month = datetime.now().month
#     this_week_num = datetime.date(datetime.utcnow()).isocalendar()[1]

# this_year = datetime.now().year
# this_week_num = datetime.date(datetime.utcnow()).isocalendar()[1]
# if this_week_num == 1:
#     last_week_of_year = datetime(this_year-1, 12, 31).isocalendar()[1]
#     getDateObjForWeekNum(last_week_of_year, this_year-1)
# else: 
#     getDateObjForWeekNum(this_week_num-1, this_year)