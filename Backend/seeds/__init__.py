"""
**The seeds package**

Contains the files necessary to seed the development database with fake users, messages, and logs. This can be very useful for testing and visualization.

--------------------------------------

**seed_all.py** is the master script that runs the seed scripts from other files. 

A good part of the data used for seeding in is json files inside the *files* directory. *seed_all.py* will check whether these files exist. If they don't, *create_seed_files.py* will be called to generate them.

*seed_users.py* will use these files to insert dummie users to the database. 
*seed_logs.py* seeds the database with fake log entries.
*seed_messages.py* shall add messages to the database, as if they had been sent through the contact form.
"""

# Seed data directory
#├── seeds/
#│   ├── files/ 
#│   │   └── create_seed_files.py         
#│   ├── __init__.py
#│   ├── helpers.py      
#│   ├── seed_all.py      # <----- Master script to run all seed scripts
#│   ├── seed_logs.py
#│   ├── seed_messages.py
#│   └── seed_users.py