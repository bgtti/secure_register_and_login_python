"""
**ABOUT THIS FILE**

TODO

"""
# Utilities
from app.constants.validation_name import RESERVED_NAMES


def user_name_is_valid(name:str) -> bool:
    """
    Validates the given username by checking if it contains any reserved words.
    Use this function to allow or block a registration or name change requested by the user.
    **What it does not do:** 
    - character and length check: this filtering is expected from Json Schema.
    - check for profanity or html: since this type of filtering is error-prone, it is not performed here.

    :param name: the name to validade
    
    Returns:
        bool: False if the name contains a reserved word, True otherwise.

    Example usage:
    ```python
        print(user_name_is_valid("AdminUser"))  # Should return False
        print(user_name_is_valid("ValidName"))  # Should return True
    ```

    """
    if not isinstance(name, str):
        raise ValueError("The provided name must be a string. Name validation failed.")

    lower_case_name = name.lower()

    for reserved in RESERVED_NAMES:
        if reserved.lower() in lower_case_name:
            return False

    return True