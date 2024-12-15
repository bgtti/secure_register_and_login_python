from bs4 import BeautifulSoup
from app.utils.constants.account_constants import COMMON_XSS_VECTORS
import logging

def check_for_html(data: str, route: str, user_email: str = "none") -> bool:
    """
    Checks for HTML content or common XSS vectors in the provided data.

    This function examines user-provided data for potential HTML input or malicious XSS patterns. 
    If such content is detected, it logs the event to the system log. The function requires the
    data input and the route from which the input was received. Optionally, the user's email
    can be included in the log for traceability.

    --------------------------------------------------------------------

    **Note:** 
    - This function should NOT be used on password input. 
    - Logging raw or unhashed passwords can create severe security risks.

    **Parameters:**
        data (str): The data to be checked for html content.
        route (str): The route through which the user data was received.
        [opt] email (str): Optionally, the email of the user in question, if known.

    **Returns:**
        - `False` if data does not contain html or if an error with the parser occurred.
        - `True` if data contains html.

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
    try:
        soup = BeautifulSoup(data, "html.parser")
        # Check if the data contains any HTML tags
        if soup.find():
            logging.warning(f"Possible HTML detected in {route}. User: {user_email}, Data supplied: {data}")
            return True
        else:
            # Check for common XSS vectors
            if any(xss_vector in data for xss_vector in COMMON_XSS_VECTORS):
                logging.warning(f"Possible XSS vector detected in {route}. User: {user_email}, Data supplied: {data}")
                return True

            return False

    except Exception as e:
        logging.error(f'Error while parsing HTML: {e}')
        return False