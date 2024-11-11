"""
**ABOUT THIS FILE**

auth/helpers.py contains the following helper function(s):

- **is_good_password**: 
- **login_schema** 

------------------------
## More information

These schemas are passed in to `validate_schema` (see `app/utils/custom_decorators/json_schema_validator.py`) through the route's decorator to validate client data received in json format by comparing it to the schema rules.

"""
import re
from app.utils.constants.account_constants import MOST_COMMON_PASSWORDS

def is_good_password(password):
    """
    is_good_password(password: str) -> bool
    ---------------------------------------

    Defines whether a password is weak or strong.
    It will search it in a list of most common passwords and check for character repetition.

    **Returns:**
        - `False` if password is weak.
        - `True` if password is strong.
    ---------------------------------------
    **Example usage:**
    ```python
        password_to_check = "SecurePassword123"
        if is_good_password(password_to_check):
            print("Password is valid!")
        else:
            print("Password is invalid.")
    ```
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