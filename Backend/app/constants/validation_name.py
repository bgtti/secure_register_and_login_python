"""
`validation_name.py` contains the list RESERVED_NAMES which is a blacklist of names the users can assign to themselves.

Staff impersonation can be an issue. Do not allow users to register with a name that may indicate authority with the site.

The list bellow should be adapted according the context your app operated. Eg: a blog may include "author" or "reviewer" to this list.

Change the first value of this list to the name of your app.

For more information about the topic, check out OWASP's recommentations available here: 
https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account
"""
RESERVED_NAMES = [
    "safedev", # TODO: change this string with your app's name
    "admin",
    "administrator",
    "customer",
    "moderator",
    "service"
    "staff"
    "personnel"
]
"""`RESERVED_NAMES` is a list of reserved names that should not be used when users attempt to create an account or change their names."""