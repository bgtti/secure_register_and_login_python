# MPTE: Choice of password length: bcrypt has a maximum length input of 72-bytes.
# Pepper (4chars) and Salt (8chars) are added to password before hashing.
# If 72 bytes is aprox the same amount in characters, 72 - 4 - 8 = 60.

INPUT_LENGTH = {
    "name": {
        "minValue": 1,
        "maxValue": 200
    },
    "email": {
        "minValue": 3,
        "maxValue": 320
    },
    "password": {
        "minValue": 8, #if this value is changed, otp must be changed
        "maxValue": 60
    },
    "otp": {
        "minValue": 8,
        "maxValue": 8
    },
    "contact_message":{
        "minValue": 1,
        "maxValue": 300
    },
    "contact_message_subject":{
        "minValue": 1,
        "maxValue": 45
    },
    "contact_message_answer_subject":{
        "minValue": 1,
        "maxValue": 50
    },
    "honeypot":{
        "minValue": 0,
        "maxValue": 15
    },
    "signed_token":{
        "minValue": 40, # consider 100. Test first though.
        "maxValue": 300, # consider 200. Test first though.
    },
    "encrypted_email":{
        "minValue": 10, # consider 100. Test first though.
        "maxValue": 390, 
    },
    "user_agent": {
        "minValue": 0, 
        "maxValue": 255 #TODO get regex pattern
    }
}
"""`INPUT_LENGTH` is a dictionary containing the minimum and maximum input length for a number of variables that can be received in json or stored in the database.

The keys: "name", "email", "password", "contact_message", "contact_message_subject", "contact_message_answer_subject", "honeypot", "signed_token", "encrypted_email", "user_agent"
"""

# Explanation of the NAME_PATTERN:
# ^ asserts the start of the string.
# [A-Za-zÀ-ÖØ-öø-ÿ .\'-] defines a character class that allows letters, spaces, accented characters, dots, apostrophes, and hyphens.
# + means one or more of the preceding characters.
# $ asserts the end of the string.
NAME_PATTERN = r'^[A-Za-zÀ-ÖØ-öø-ÿ .\'-]+$'
"""`NAME_PATTERN` is a regex to define the name of a user."""

# Explanation of the EMAIL_PATTERN:
# ^: Asserts the start of the string.
# [^@\s]+: Matches one or more characters that are not '@' or whitespace.
# @: Matches the '@' character.
# [^@\s]+: Matches one or more characters that are not '@' or whitespace.
# $: Asserts the end of the string.
EMAIL_PATTERN = r'^[^@\s]+@[^@\s]+$'
"""`EMAIL_PATTERN` is a regex to define the email format of a user."""

PASSWORD_PATTERN = r'^[\s\S]{%d,%d}$' % (INPUT_LENGTH['password']['minValue'], INPUT_LENGTH['password']['maxValue'])
"""`PASSWORD_PATTERN` is a regex to define the password format of a user (and specifies size constraints)."""

OTP_PATTERN = r'^\d{8}$' 
"""`OTP_PATTERN` is a regex to define the otp format (and specifies size constraint of 8 digits). Otp would be a string."""

DATE_PATTERN =r'^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$'
"""`DATE_PATTERN` is a regex to define the accepted format of YYYY-MM-DD dates."""

# Most common password list based on: https://nordpass.com/most-common-passwords-list/
# IMPORTANT:
# The name of the app in question is commonly used in passwords. 
# TODO Substitute the first value of the list with the name of your app if you are using this template.
# Use lower case letters only, as a string will be compared to a value in this list in lower case.
MOST_COMMON_PASSWORDS = [
    "safedev",
    "1q2w3",
    "102030",
    "112233",
    "445566",
    "12345",
    "54321",
    "abc123",
    "abcd",
    "admin",
    "asdfghjkl",
    "azerty",
    "demo",
    "eliska81",
    "iloveyou",
    "monkey",
    "p@ssw0rd",
    "pass@123",
    "password",
    "qwerty",
    "root",
    "superman",
    "ubnt",
    "unknown",
    "user",
    "qwerty",
    "yxcvbnm"
]
"""`MOST_COMMON_PASSWORDS` is a list of easy-to-guess passwords that should not be accepted"""

# there are a number of events in js that could be part of the list bellow... checkout http://help.dottoro.com/ljfvvdnm.php for more.
COMMON_XSS_VECTORS = [
    "alert",
    "confirm",
    "data",
    "decode",  # decode.URI
    "document",  # "document.cookie"
    "dynsrc",
    "eval",
    "expression",
    "fromCharCode",
    "href",
    "html",
    "iframe",
    "img",
    "location",
    "onchange",
    "onclick",
    "onerror",
    "onfocus",
    "onload",
    "onmouseover",
    "prompt",
    "script", # catches also "javascrip"
    "src", # "lowscr"
    "svg",
    "textarea",
    "unescape",
    "window",
    "&lt", # <
    "&gt", # >
    "&quot;" # "
    "&#x3C", # <
    "&#x3E;", # >
    "%3C", # <
    "%3E", # >
    "u003", # < for \u003C, \u003E, %u003C, and %u003E
    ".js",
    "$env"
]
"""`COMMON_XSS_VECTORS` is a black list of words that may indicate an injection attempt."""

# staff impersonation can be an issue. Do not allow users to register with a name that may indicate authority with the site.
# the list bellow should be adapted according the context your app operated. Eg: a blog may include "author" or "reviewer" to this list.
# NOTE OWASP recommendation: https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account
# TODO if you are using this template: change the first string with the apps' name
RESERVED_NAMES = [
    "safedev",
    "admin",
    "administrator",
    "moderator",
    "customer",
    "service"
]
"""`RESERVED_NAMES` is a list of reserved names that should not be used when users attempt to create an account or change their names."""
