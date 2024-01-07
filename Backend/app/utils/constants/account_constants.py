# Choice of password length: bcrypt has a maximum length input of 72-bytes.
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
        "minValue": 8,
        "maxValue": 60
    }
}

#Most common password list based on: https://nordpass.com/most-common-passwords-list/
# IMPORTANT:
# The name of the app in question is commonly used in passwords. 
# Substitute the first value of the list with the name of your app if you are using this template.
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

EMAIL_PATTERN = r'^[^@\s]+@[^@\s]+$'
PASSWORD_PATTERN = r'^[\s\S]{%d,%d}$' % (INPUT_LENGTH['password']['minValue'], INPUT_LENGTH['password']['maxValue'])

# Explanation of the EMAIL_PATTERN:
# ^: Asserts the start of the string.
# [^@\s]+: Matches one or more characters that are not '@' or whitespace.
# @: Matches the '@' character.
# [^@\s]+: Matches one or more characters that are not '@' or whitespace.
# $: Asserts the end of the string.

# Explanation of the PASSWORD_PATTERN:
# ^: Asserts the start of the string.
# [\s\S]: Matches any character, including whitespace (ASCII and Unicode).
# {%d,%d}: Specifies the minimum and maximum length based on your constants.
# $: Asserts the end of the string.