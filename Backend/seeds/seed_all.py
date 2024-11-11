# Master script to run all seed scripts
"""
**ABOUT THIS FILE**

seed_all.py seeds the database with:
- users
- messages
- logs

for the purpose of testing in development.
It will call the main functions from *seed_logs.py", "seed_messages.py", and "seed_users.py" to acomplish this.
"""

#TODO REPLACE CONSOLE_WARN

import os
from app.extensions import db
from app.models.user import User
from utils.print_to_terminal import print_to_terminal
from seeds.seed_logs import create_dummie_logs
from seeds.seed_messages import create_dummie_messages
from seeds.seed_users import create_dummie_user_accts
from seeds.files.create_seed_files import create_seed_files, SEED_FILES_JSON

def seed_database():
    # Check if Dummy users exist in the database already; if they do, no need to re-seed the db
    seeds_exist = db.session.query(User).get(2)

    if seeds_exist:
        return
    
    # Check if any json file is not found and create them if necessary
    if any(not os.path.exists(f"seeds/files/{file_name}") for file_name in SEED_FILES_JSON):
        print_to_terminal("Creating files for base seed data.", "CYAN")
        create_seed_files()

    print_to_terminal("Seeding the database. This may take a few seconds...", "CYAN")
    create_dummie_user_accts()
    print_to_terminal("...seeding the db with logs...", "CYAN")
    create_dummie_logs()
    print_to_terminal("...seeding the db with messages...", "CYAN")
    create_dummie_messages()
    print_to_terminal("Seeding completed: 100 users were added to the database!", "CYAN")
    print()
    print_to_terminal("Happy coding!", "GREEN")
    print()