# Python &Flask
import logging
import re

# Extensions
from bs4 import BeautifulSoup

# Constants
from app.constants.xss_vectors import COMMON_XSS_VECTORS

# Other helpers
from app.common.log_utils.log_data_sanitation import safe_to_log


def check_for_html(data: str, route: str, user_email: str = "") -> bool:
    """
    Checks whether user input appears to contain HTML or common XSS-like vectors.

    This is a lightweight detection/flagging helper, not a complete XSS
    prevention mechanism. It should be used to flag suspicious input for
    moderation/logging, while output escaping and sanitization should still
    be handled wherever user content is rendered.

    **Do not use this function on password fields.**

    Returns:
        bool:
            True if suspicious HTML/XSS-like content is detected.
            False otherwise.

    :param data (str): The data to be checked for html content.
    :param route (str): The route through which the user data was received.
    :param [opt] email (str): Optionally, the email of the user in question, if known.

    --------------------------------------------------------------------
    **Example usage:**
    
    Example usage 1: 
    ```python
    check_for_html("<base href='http://example.com/'>", "signup: name field input")
    # Returns -> True
    ```

    Example usage 2:
    ```python
    check_for_html("John", "signup: name field input")
    # Returns -> False
    ``` 
    """
    if not data:
        return False
    
    if not route:
        route = "unknown"
    
    if not user_email:
        user_email = "unknown"
    else:
        # anonymize
        first_2_chars = user_email[:2]
        remainder = user_email[2:]
        anonymized_remainder = re.sub(r'[a-zA-Z0-9À-ÖØ-öø-ÿ]', '*', remainder )
        user_email = first_2_chars + anonymized_remainder
    
    try:
        soup = BeautifulSoup(data, "html.parser")
        # Check if the data contains any HTML tags
        if soup.find():
            logging.warning(f"Possible HTML detected in {route}. User: {user_email}.")
            return True
        
        # Check for common XSS vectors
        normalized_data = data.lower()
        if any(vector in normalized_data for vector in COMMON_XSS_VECTORS):
            # Sanitize prior to logging
            data = safe_to_log(data)
            logging.warning(f"Possible XSS vector detected in {route}. User: {user_email}. Data supplied (special chars replaced with *): {data}")
            return True

        return False

    except Exception as e:
        logging.error(f'Error while parsing HTML in check_for_html function: {e}')
        return False