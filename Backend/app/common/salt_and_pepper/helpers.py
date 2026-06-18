import random
from datetime import datetime
from uuid import uuid4
from config.values import PEPPER

# function to get pepper according to account creation date
def get_pepper(date):
    """
    get_pepper(date: datetime) -> str[4]
    --------------------------------------

    Requires a datetime argument. 
    Returns one of the strings defined in PEPPER (from the configuration files). 

    --------------------------------------
    **Important:**

    Make sure you have the pepper array in the env file like: 
    
    `PEPPER = '["xxxx", "xxxx", "xxxx", "xxxx", "xxxx", "xxxx"]'` 
    
    where xxxx represents a random 4-char string.

    The month inside the date string will define which pepper value will be returned.

    --------------------------------------
    Example usage:

    `date = datetime.utcnow()` 

    `pepper = get_pepper(date)` 

    *if in config `PEPPER = ["xxx0", "xxx1", "xxx2", "xxx3", "xxx4", "xxx5"]`, then:*

    - **January and July**: `pepper = "xxx0"`
    - **February and August**: `pepper = "xxx1"`
    - **March and September**: `pepper = "xxx2"`
    - **April and October**: `pepper = "xxx3"`
    - **May and November**: `pepper = "xxx4"`
    - **June and December**: `pepper = "xxx5"`
    """
    pepper = PEPPER[(date.month -1) % len(PEPPER)] 
    return pepper


# Function to generate a random 8-character string to salt user passwords
def generate_salt():
    """
    generate_salt() -> str[8]
    --------------------------------

    Accepts no arguments and returns a radom 8-character string.

    --------------------------------
    Example usage:
    `salt = generate_salt()`
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

