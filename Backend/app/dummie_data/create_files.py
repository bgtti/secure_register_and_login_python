import random
import string
from uuid import uuid4
import ipaddress
from app.extensions import faker
import os
import json

"""
A dummie user is created based on a list of random names.

for every user created:
    - one user stats is also created (since this table keeps track of every account created or deleted)
    - 2 visitor stats are created: page_accessed = "home", and page_accessed = "signup" (since we can assume every user who created an account visited those two pages)

Also, random visitor stats are created (2x the number of users created). These are meant to simulate random visitors to the website who did not create an account.

The data and functions in this file were used to create the following files:
    - data_users.json -> will populate the users database
    - data_user_stats.json -> will populate the user stats database (correlate to users created)
    - data_users_visitor_stats.json -> will populate the visitor stats database (correlate to users created)
    - data_visitor_stats.json -> will populate the visitor stats database (correlate to users created)

create_dummie_files() is the function that created these files - and it was called from dummie_users.py once.
If the json files are deleted and no second db User is found, the files will be re-created if the code runs in development mode.
Check dummie_users.py (in this directory) to see how the data in this page is called and how the files are used.
"""

# BASE INFORMATION FOR DUMMIE DATA CREATION

dummie_names = ["James Maung", "Robert Lu", "Patricia Khan", "Dorothy", "James Ali", "Mary Kumar", "Robert Singh", "Patricia Devi", "John Zhang", "Jennifer Wang", "Michael dos Santos", "Linda Schmidt", "David Schneider", "Elizabeth Becker", "William Bauer", "Barbara Dubois", "Richard Leroy", "Susan Bruno", "Joseph Ricci", "Jessica Marino", "Thomas Colombo", "Sarah Ferrari", "Jason", "Christopher Bianchi", "Karen Nagy", "Charles Szabó", "Lisa Kovács", "Daniel Jansen", "Matthew Vanderberg", "Betty Almeida", "Sandra Carvalho", "Mark Oni", "Melissa", "Margaret Taiwo", "Donald Zabu", "Ashley Simpson", "Steven Tyjani", "Andrew Badenhorst", "Emily Nel", "Paul van der Merwe", "Donna Asrat", "Joshua Tamesgen", "Kenneth Hassan", "Kevin Adel", "Amanda Ahmad", "George", "Brian Abdallah", "Deborah", "Anna Scott", "Nicole Roberts", "Brandon Carter", "Samantha Mitchell", "Brenda", "Benjamin Campbell", "Katherine Rivera", "Shirley", "Samuel Hall", "Christine Baker", "Gregory Nelson", "Helen Adams", "Alexander Green", "Debra Flores", "Patrick Hill", "Rachel Nguyen", "Frank Torres", "Carolyn Scott", "Stephanie O", "Nicholas", "Peter Hernandez", "Raymond Wright", "Janet King", "Jack Allen", "Maria Young", "Dennis Walker", "Kyle Rodriguez", "Catherine Robinson", "Jerry Lewis", "Heather Ramirez", "Tyler Clark", "Aaron Harris", "Olivia White", "Jose Thompson", "Adam Lee", "Nathan Jackson", "Victoria Moore", "Henry Taylor", "Ruth Thomas", "Zachary Anderson", "Virginia Wilson", "Douglas Gonzalez", "Lauren Lopez", "Kelly Martinez", "Christina Davis", "Noah Garcia", "Joan Miller", "Ethan Jones", "Evelyn Brown", "Jeremy Williams", "Judith Johnson", "Walter Smith"]

dummie_places = [
    ("Africa", "Egypt", "EG", "Cairo"),
    ("Africa", "Nigeria", "NG", "Lagos"),
    ("Africa", "South Africa", "ZA", "Cape Town"),
    ("Africa", "South Africa", "ZA", "Johannesburg"),
    ("Asia", "India", "IN", "Mumbai"),
    ("Asia", "India", "IN", "Jaipur"),
    ("Asia", "Indonesia", "ID", "Jakarta"),
    ("Asia", "Japan", "JP", "Tokio"),
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
    ("South America", "Chile", "CL","Valparaiso"),
    ("South America", "Colombia", "CO","Bogota"),
    ("South America", "Uruguay", "UY","Montevideo"),
    ("Oceania", "Australia", "AU","Sydney"),
    ("Oceania", "Australia", "AU","Melbourne"),
]

dummie_referrer = [
    "", # mimics direct traffic (or Referer header missing, or empty string)
    "https://thiswebsite.com/internal-page" # mimics internal page link
    "",
    "https://thiswebsite.com/previous-page", # mimics internal page link
    "",
    "https://exampleblog.com/page?q=123", # mimics external source (blog)
    "",
    "https://examplereferrer.com/", # mimics external source (some website redirect)
    "",
    "https://social-network.example", # mimics external source (social media)
    "",
    "https://www.google.com/search?q=query", # mimics external source (search query)
    "",
    "https://external-site.com/some-page", # mimics external source (some website's link clicked)
    "",
    
]

# Listed website pages, weighted according to the likelyhood of being accessed
weighted_page_accessed = {
    "home": 6,
    "login": 3,
    "signup": 3,
    "about": 2,
    "contact": 2,
    "faq": 2,
    "privacy-policy": 1,
    "cookie-policy": 1,
    "terms-and-conditions": 1,
    "error": 1,
    "admin-login": 1,
}

# HELPER FUNCTIONS FOR DUMMIE DATA CREATION:

def generate_fake_str():
    """
    generate_fake_str(:void) -> str
    ----------------------------------------------------------------------------
    This function takes no arguments and returns a random 8-character string.
    The string may be comprised of uppercase and lower case letters and numbers
    ----------------------------------------------------------------------------
    Example usage:

    print(generate_fake_str()) -> prints to console: ReytT30t
    random_str = generate_fake_str() -> random_str is "k4XMlsXo"
    salt = generate_fake_str() -> salt is "KJzOUfcS"
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

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

def get_uuid():
    """
    get_uuid(:void) -> str
    --------------------------------
    This function generates a uuid.
    --------------------------------
    Example usage:
    
    my_uuid = get_uuid()
    """
    return uuid4().hex

def fake_anonymize_ip(ip_address):
    """
    fake_anonymize_ip(ip_address: str) -> str
    --------------------------------------------
    This function anonymizes fake ipv4 data.
    --------------------------------------------
    Example usage:
    
    fake_anonymize_ip("192.168.1.100") -> "192.168.1.0"
    """
    ip = ipaddress.ip_address(ip_address)
    return ".".join(str(octet) for octet in ip.packed[:-1]) + ".0"

def create_dummie_visitor_stats():
    """
    create_dummie_visitor_stats(:void) -> dict[str, str]
    -----------------------------------------------------
    This creates an object with fake visitor stats data.
    Used in create_dummie_files().
    """
    random_referrer_index = random.randint(0,len(dummie_referrer)-1) 
    visitor_session_id = get_uuid()
    random_location_index = random.randint(0,len(dummie_places)-1)
    page = random.choices(list(weighted_page_accessed.keys()), weights=list(weighted_page_accessed.values()))[0]
    model_visitor_stats_random = {
        "ip_address": fake_anonymize_ip(faker.ipv4()) ,
        "continent": dummie_places[random_location_index][0],
        "country": dummie_places[random_location_index][1],
        "country_code": dummie_places[random_location_index][2],
        "city": dummie_places[random_location_index][3],
        "user_agent": faker.user_agent(),
        "screen_size": "(0 x 0)",
        "referrer": dummie_referrer[random_referrer_index],
        "page_accessed": page,
        "session_visit": visitor_session_id,
        "date_accessed": ""
    }
    return model_visitor_stats_random

# DUMMIE DATA CREATION:

def create_dummie_files():
    """
    create_dummie_files(:void) -> IO
    --------------------------------------------------------------------------------
    This function takes no arguments and generates 4 python files containing 
    lists of dictionaries.

    This function generated the dummie data used to created the database for testing.
    By creating the files with the dummie data in advance, it was possible to speed
    things up a little bit when creating the dummie users at run time, and allows the 
    create user file to be a little shorter.
    """
    user_list = []
    user_stats_list = []
    visitor_stats_list = []
    visitor_stats_random = []

    for name in dummie_names:
        # dummie user data
        model_user = {
            "name": name,
            "email": generate_fake_mail(name),
            "password": generate_fake_str(),
            "salt": generate_fake_str(),
            "created_at": "", # populated at runtime when creating dummie users
            # "session": "", # leave empty
            "last_seen":"", # populated at runtime when creating dummie users
        }
        user_list.append(model_user)
        # dummie user stats data
        random_location_index = random.randint(0,len(dummie_places)-1)
        model_user_stats = {
            "year": "", # populated at runtime when creating dummie users
            "month": "", # populated at runtime when creating dummie users
            "week": "", # populated at runtime when creating dummie users
            "new_user": 1, # when user created it is 1
            "country": dummie_places[random_location_index][1]
        }
        user_stats_list.append(model_user_stats)
        # dummie visitor stats data (2x per user created)
        random_referrer_index = random.randint(0,len(dummie_referrer)-1) 
        visitor_session_id = get_uuid()
        model_visitor_stats = {
            "ip_address": fake_anonymize_ip(faker.ipv4()),
            "continent": dummie_places[random_location_index][0],
            "country": dummie_places[random_location_index][1],
            "country_code": dummie_places[random_location_index][2],
            "city": dummie_places[random_location_index][3],
            "user_agent": faker.user_agent(),
            "screen_size": "(0 x 0)",
            "referrer": dummie_referrer[random_referrer_index],
            "page_accessed": "home",
            "session_visit": visitor_session_id,
            "date_accessed": "" # populated at runtime when creating dummie users
        }
        visitor_stats_list.append(model_visitor_stats)
        model_visitor_stats2 = model_visitor_stats.copy()
        model_visitor_stats2["page_accessed"] = "signup"
        model_visitor_stats2["referrer"] = "https://thiswebsite.com/home"
        visitor_stats_list.append(model_visitor_stats2)

    for i in range(len(visitor_stats_list)):
        # dummie visitor stats data (adding some random extra data)
        model_visitor_stats_random = create_dummie_visitor_stats()
        visitor_stats_random.append(model_visitor_stats_random)
        
    file_paths = [
            "data_users.json",
            "data_users_stats.json",
            "data_users_visitor_stats.json",
            "data_visitor_stats.json",
        ]

    data_to_write = [
        user_list,
        user_stats_list,
        visitor_stats_list,
        visitor_stats_random,
    ]
    
    for i in range(len(file_paths)):
        with open(os.path.join(os.path.dirname(__file__), file_paths[i]), "w", encoding="utf-8") as file:
            json.dump(data_to_write[i], file, indent=4)  # Use json.dump to write the data as JSON
    

# The function above used to create .py files. In case you prefer .py over .json, here are the original bits:
    # file_paths = [
    #         "data_users.py",
    #         "data_users_stats.py",
    #         "data_users_visitor_stats.py",
    #         "data_visitor_stats.py",
    #     ]
    # data_to_write = [
    #     (user_list, 'user_list'),
    #     (user_stats_list, 'user_stats_list'),
    #     (visitor_stats_list, 'visitor_stats_list'),
    #     (visitor_stats_random, 'visitor_stats_random'),
    # ]
    # for i in range(len(file_paths)):
    #     with open(os.path.join(os.path.dirname(__file__), file_paths[i]), "w", encoding="utf-8") as file:
    #         # if i != 1:
    #         #     file.write(f"import datetime\n")
    #         file.write(f"{data_to_write[i][1]} = {data_to_write[i][0]}")