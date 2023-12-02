import random
import string
import datetime
from uuid import uuid4

# Function to generate a random 8-character string to salt user passwords
def generate_salt():
    """Function generates a random 8-character salt."""

    # Getting first random character: from a timestamp
    current_datetime = datetime.datetime.now()
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

# Alternative
# This function was based on an answer from StackOverflow: https://stackoverflow.com/a/2257449
def generate_random():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))




