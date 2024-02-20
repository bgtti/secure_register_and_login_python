from bs4 import BeautifulSoup
from app.utils.constants.account_constants import COMMON_XSS_VECTORS
import logging

def check_for_html(data, route, user_email="none"):
    """
    check_for_html(data: str, route: str, opts: user_email=str) -> bool
    ----------------------------------------------------------------------------------------------------------------------
    Function checks data for html input and common XSS vectors, will log it to system_log if it is found, and will return true or false.
    Requires the data input and the route which received it. 
    If user_email is known, it can be provided - and this will be included in the log.
    DO NOT use this function on password input!
    Passwords - especially raw and unhashed - would be logged, becomming a big security risk!
    ----------------------------------------------------------------------------------------------------------------------
    Example usage 1: 
    check_for_html("<base href='http://example.com/'>", "signup: name field input")
    -> True

    Example usage 2: 
    check_for_html("John", "signup: name field input") -> False
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