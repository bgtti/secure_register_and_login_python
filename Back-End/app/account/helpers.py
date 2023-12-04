import re
from app.account.constants import MOST_COMMON_PASSWORDS
from datetime import datetime

def is_good_password(password):
    # Check for sequential repetition
    sequential_repetition_pattern = r"(\S)\1{3,}"  # Matches any character repeated 4 or more times
    if re.search(sequential_repetition_pattern, password):
        return False

    # Check for common passwords only if the password is 15 characters or less
    if len(password) <= 15 and any(common_password in password for common_password in MOST_COMMON_PASSWORDS):
        return False

    # If the password passes both checks, it is considered valid
    return True

# Example usage
# password_to_check = "SecurePassword123"
# if is_good_password(password_to_check):
#     print("Password is valid!")
# else:
#     print("Password is invalid.")

