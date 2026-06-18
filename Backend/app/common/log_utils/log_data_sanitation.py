# Python & Flask
import re

def safe_to_log(data: str) -> str:
    """
    Can be used to sanitize user input prior to logging.
    Will output a string that is safe to log.
    
    - Ensure the string has a max of 300 chars
    - Removes line breaks and controls (\\r, \\n, \\t )
    - Replaces certain special characters with *

    Characters that will be replaced: / \ | $ : { [ ( ' " ` # < % + = ;

    **Remember not to log passwords and OTPs**

    :param data (str): The data to be sanitized.

    Returns:
        str: the data stripped of special characters, safe for logging.

    **Example usage:** 
    
    ```python
    user_input = "https://app.com[INFO]+User:+admin+deleted+all+files"
    safe_input = safe_to_log(user_input)
    # Returns -> "https***app.com*INFO]*User:*admin*deleted*all*files"

    user_input = "one%0a%0aINFO:+User+logged+out%3dbad"
    safe_input = safe_to_log(user_input)
    # Returns -> "one*0a*0aINFO**User*logged*out*3dbad"
    ```
    """
    if not data:
        return data
    
    data = str(data)[:300]
    data = re.sub(r"[\r\n\t\x00-\x1f\x7f-\x9f]", " ", data)
    data = re.sub(r"[\/\\|$:{\[\('\"`#<%+=;]", "*", data)
    return data
    