import os
import ast
import random
import logging
from datetime import datetime
from uuid import uuid4

# Pepper requires a pepper array set in an env file
PEPPER_STRING_ARRAY = os.getenv('PEPPER')
# If it does not exist or it is set up incorrectly, a default version will be used so that the code does not break.
try:
    PEPPER_ARRAY = ast.literal_eval(PEPPER_STRING_ARRAY)
    if not isinstance(PEPPER_ARRAY, list) or len(PEPPER_ARRAY) != 6:
        raise ValueError("PEPPER must have exactly 6 values.")
except (ValueError, SyntaxError, TypeError):
    logging.error("Error reading PEPPER. Using fallback pepper array.")
    PEPPER_ARRAY = ["xYz1", "XyZ2", "zXy5", "ZxY9", "7Zyx", "Y8zX"]

# function to get pepper according to account creation date
def get_pepper(date):
    """
    get_pepper(date: datetime) -> str[4]
    --------------------------------------
    Requires a datetime argument. 
    Returns a string defined in the
    PEPPER saved in the env file. 
    --------------------------------------
    Important:
    Make sure you have the pepper array in
    the env file like: PEPPER = '["xxxx", 
    "xxxx", "xxxx", "xxxx", "xxxx", 
    "xxxx"]' where xxxx represents a
    random 4-char string.
    --------------------------------------
    Example usage 1:
    date = datetime.utcnow()
    pepper = get_pepper(date)

    Example usage 2:
    date = user.created_at #from db model
    pepper = get_pepper(date)
    """
    pepper = PEPPER_ARRAY[(date.month -1) % len(PEPPER_ARRAY)] 
    return pepper


# Function to generate a random 8-character string to salt user passwords
def generate_salt():
    """
    generate_salt() -> str[8]
    --------------------------------
    Accepts no arguments and returns 
    a radom 8-character string.
    --------------------------------
    Example usage:
    salt = generate_salt()
    """
    # Getting first random character: from a timestamp
    current_datetime = datetime.now()
    # Convert the datetime to a numeric value (Unix timestamp)
    timestamp = int(current_datetime.timestamp())
    timestamp_string = str(timestamp)
    rand_num= random.randint(0, len(timestamp_string)-1)
    random_char_1 = timestamp_string[rand_num]
    # Getting second and third random character: Create an ASCII character from UUID4
    uuid = uuid4()
    # Extract the first byte of the UUID as an integer
    uuid_integer = int.from_bytes(uuid.bytes[:1], byteorder='big')
    # Map the integer to the range [33, 126], which correspond to ASCII characters
    random_number_2 = 33 + (uuid_integer % (126 - 33 + 1))
    # Map the integer to the range [33, 64], which correspond to ASCII symbol characters
    random_number_3 = 33 + (uuid_integer % (64 - 33 + 1))
    # Convert the random number to the corresponding ASCII character
    random_char_2 = chr(random_number_2)
    random_char_3 = chr(random_number_3)
    # Getting fourth to eith randi character: From second UUID4
    uuid_hex = uuid4().hex #32 characters (without '-')
    # Get random character string
    random_chars = random_char_1 + random_char_2 + random_char_3 + uuid_hex[5] + uuid_hex[8] + uuid_hex[27] + uuid_hex[random.randint(0, 31)]
    # Schuffle string with original state of the random number generator
    pw_salt = ''.join(random.sample(random_chars,len(random_chars)))
    # Return 8 characters
    return pw_salt[:8]

# Alternative - if you find the function above (salt creation) an overkill:
# The function bellow is based on an answer from StackOverflow: https://stackoverflow.com/a/2257449
# import string
# def generate_salt():
#     return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

