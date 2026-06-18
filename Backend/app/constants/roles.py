"""
Docstring for Backend.app.constants.roles
in ROLES array, changing the name will not impact the app: name is for presentation purposes only.
Changing the value of "access_level" will

roles array used to create the Role db model.
"""

ROLES = [
    {
        "id": 1,
        "name": "User",
        "access_level": "user"
    },
    {
        "id": 2,
        "name": "Admin",
        "access_level": "admin"
    },
    {
        "id": 3,
        "name": "Super Admin",
        "access_level": "super_admin"
    },
    # {
    #     "id": 4,
    #     "name": "Support",
    #     "access_level": "customer_support"
    # },
    # {
    #     "id": 5,
    #     "name": "Content Writer",
    #     "access_level": "content_writer"
    # },
    # {
    #     "id": 6,
    #     "name": "Tech Writer",
    #     "access_level": "tech_writer"
    # },
    # {
    #     "id": 7,
    #     "name": "Developer",
    #     "access_level": "developer"
    # },
]