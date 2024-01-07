import re
from app.utils.constants.account_constants import MOST_COMMON_PASSWORDS

def is_good_password(password):
    """
    is_good_password(password: str) -> bool
    ---------------------------------------
    Returns:
        False if password is weak.
        True if password is strong.
    ---------------------------------------
    Example usage:
    password_to_check = "SecurePassword123"
    if is_good_password(password_to_check):
        print("Password is valid!")
    else:
        print("Password is invalid.")
    """
    # Check for sequential repetition
    sequential_repetition_pattern = r"(\S)\1{3,}"  # Matches any character repeated 4 or more times
    if re.search(sequential_repetition_pattern, password):
        return False

    # Check for common passwords only if the password is 15 characters or less
    if len(password) <= 15 and any(common_password in password for common_password in MOST_COMMON_PASSWORDS):
        return False

    # If the password passes both checks, it is considered valid
    return True