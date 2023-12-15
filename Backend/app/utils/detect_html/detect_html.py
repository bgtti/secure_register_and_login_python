from bs4 import BeautifulSoup
import logging

def check_for_html(data, route, ip_address="none", user_email="none"):
    """
    check_for_html(data: str, route: str, opts: ip_address=str, user_email=str) -> bool
    ----------------------------------------------------------------------------------------------------------------------
    Function checks data for html input, will log it to system_log if it is found, and will return true or false.
    Requires the data input and the route which received it. 
    If user_email and/or ip_address is known, it can be provided - and this will be included in the log.
    DO NOT use this function on password input!
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
            logging.warning(f"Possible HTML detected in {route}. IP: {ip_address}, User: {user_email}, Data supplied: {data}")
            return True
        else:
            return False
    except Exception as e:
        logging.error(f'Error while parsing HTML: {e}')