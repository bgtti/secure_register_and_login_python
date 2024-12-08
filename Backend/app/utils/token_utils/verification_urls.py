"""
**ABOUT THIS FILE**

verification_urls.py contains the necessary variables and function to create frontend url endpoints with tokens. 

--------------------
**Content**

The function `create_verification_url(token, purpose)` should be passed a token from the db and a purpose from the TokenPurpose enum so it can run the function for signing the token, add it to the appropriate url base and return a client-ready url that can be sent in an email to the user. The url will point to the appropriate frontend endpoint that can send a request to verify the given token.
"""
from config.values import BASE_URLS
from app.utils.token_utils.sign_and_verify import sign_token

# TODO: hardcoded links are a bad idea. The urls bellow should be transfered to a common file used by both FE and BE
BE_URL = BASE_URLS["backend"]
FE_URL = BASE_URLS["frontend"]

# TODO: build FE pages
LINK_CONFIRM_PASSWORD_CHANGE = f"{FE_URL}/setNewPw/token="
LINK_CONFIRM_EMAIL_CHANGE_OLD = f"{FE_URL}/confirmEmailChange/token="
LINK_CONFIRM_EMAIL_CHANGE_NEW = f"{FE_URL}/confirmNewEmail/token="
LINK_EMAIL_VERIFICATION = f"{FE_URL}/verifyEmail/token=" # does not exist / not yet in use! reserved for future development

purpose_urd_dic = {
    "pw_change": LINK_CONFIRM_PASSWORD_CHANGE,
    "email_change_old_email": LINK_CONFIRM_EMAIL_CHANGE_OLD,
    "email_change_new_email": LINK_CONFIRM_EMAIL_CHANGE_NEW,
    "email_verification" : LINK_EMAIL_VERIFICATION,
}

def create_verification_url(token, purpose):
    """
    create_verification_url(token:str, purpose: enum) --> str

    ----------------
    Generates a verification URL based on the purpose and token.

    **Parameters**:
        token (str): The token to include in the URL.
        purpose (enum class TokenPurpose): (e.g., TokenPurpose.PW_CHANGE)

    **Returns:**
        str: The verification URL with the signed token.
    """
    signed_token = sign_token(token, purpose)

    # Get the base URL from the dictionary
    base_url = purpose_urd_dic.get(purpose.value)
    if not base_url:
        raise ValueError(f"No URL mapped for purpose '{purpose.value}'")
    
    url = f"{base_url}{signed_token}"

    return url



