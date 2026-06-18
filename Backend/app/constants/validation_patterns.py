"""
`validation_patterns.py` contains variables that define regex patterns for certain inputs. Meant to be used definitions for input length and accepted patterns to be used in JSON schemas for validation of inputs in requests.

Available regex patterns for:
- Name: NAME_PATTERN
- Email: EMAIL_PATTERN
- OTP: OPT_PATTERN
- Dates: DATE_PATTERN
"""

NAME_PATTERN = r'^[A-Za-zÀ-ÖØ-öø-ÿ .\'-]+$'
"""`NAME_PATTERN` is a regex to define the name of a user."""
# Explanation of the NAME_PATTERN:
# ^ asserts the start of the string.
# [A-Za-zÀ-ÖØ-öø-ÿ .\'-] defines a character class that allows letters, spaces, accented characters, dots, apostrophes, and hyphens.
# + means one or more of the preceding characters.
# $ asserts the end of the string.
# ALTERNATIVELY use: NAME_PATTERN = r"^[A-Za-zÀ-ÖØ-öø-ÿĀ-ž .'-]+$"
# The above would cover most european alphabets, inlcuding hungarian

EMAIL_PATTERN = r'^[^@\s]+@[^@\s]+$'
"""`EMAIL_PATTERN` is a regex to define the email format of a user."""
# Explanation of the EMAIL_PATTERN:
# ^: Asserts the start of the string.
# [^@\s]+: Matches one or more characters that are not '@' or whitespace.
# @: Matches the '@' character.
# [^@\s]+: Matches one or more characters that are not '@' or whitespace.
# $: Asserts the end of the string.
# ALTERNATIVELY, IF THE ABOVE IS TOO PERMISSIVE:
# EMAIL_PATTERN = (
#     r"^(?!\.)"
#     r"(?!.*\.\.)"
#     r"[A-Za-z0-9._%+-]+"
#     r"@"
#     r"(?!-)"
#     r"[A-Za-z0-9.-]+"
#     r"\.[A-Za-z]{2,}$"
# )
# enforces local part: letters, numbers, . _ % + -, no leading dots, no consecutive dots
# domain part: letters, umbers, hyphen, dot, no leading hyphen, requires real TLD
# no spaces allowed, no <> " ' 

# Password pattern: I decided against a password pattern. I don't believe it to be helpful to limit characters the user can input nor force the user to use characters...
# PASSWORD_PATTERN = r'^[\s\S]{%d,%d}$' % (INPUT_LENGTH['password']['minValue'], INPUT_LENGTH['password']['maxValue'])
# """`PASSWORD_PATTERN` is a regex to define the password format of a user (and specifies size constraints)."""

OTP_PATTERN = r'^\d{8}$' 
"""`OTP_PATTERN` is a regex to define the otp format (and specifies size constraint of 8 digits). Otp would be a string."""

DATE_PATTERN =r'^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$'
"""`DATE_PATTERN` is a regex to define the accepted format of YYYY-MM-DD dates."""

