"""
`validation_password.py` contains the list MOST_COMMON_PASSWORDS.

The most common passwords list is based on NordPass's *Top 200 Most Common Passwords* [source: https://nordpass.com/most-common-passwords-list/]

Note the first value in the list is the name of the app in question.
The name of the app in question is commonly used in passwords, and this is too easy for a bad actor to guess. Substitute the first value of the list with the name of your app if you are using this template.

Including values in this list: use lower case letters only, as a string will be compared to a value in this list in lower case.
"""
MOST_COMMON_PASSWORDS = [
    "safedev", #TODO: replace with the name of your app
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
"""`MOST_COMMON_PASSWORDS` is a list of easy-to-guess passwords that should not be accepted."""