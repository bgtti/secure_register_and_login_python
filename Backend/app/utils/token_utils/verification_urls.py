"""
**ABOUT THIS FILE**

verification_urls.py contains the necessary variables and function to create frontend url endpoints with tokens. 

--------------------
**Content**

The function `create_verification_url(token, purpose)` should be passed a token from the db and a purpose from the TokenPurpose enum so it can run the function for signing the token, add it to the appropriate url base and return a client-ready url that can be sent in an email to the user. The url will point to the appropriate frontend endpoint that can send a request to verify the given token.
"""
from config.values import BASE_URLS
from app.utils.constants.enum_class import TokenPurpose
from app.utils.token_utils.sign_and_verify import sign_token

# TODO: hardcoded links are a bad idea. The urls bellow should be transfered to a common file used by both FE and BE
BE_URL = BASE_URLS["backend"]
FE_URL = BASE_URLS["frontend"]

# TODO: build FE pages
LINK_PASSWORD_RESET = f"{FE_URL}/resetPassword"
LINK_CONFIRM_PASSWORD_CHANGE = f"{FE_URL}/setNewPw"
LINK_CONFIRM_EMAIL_CHANGE_OLD = f"{FE_URL}/confirmEmailChange"
LINK_CONFIRM_EMAIL_CHANGE_NEW = f"{FE_URL}/confirmNewEmail"
LINK_EMAIL_VERIFICATION = f"{FE_URL}/verifyEmail" # does not exist / not yet in use! reserved for future development

purpose_url_dic = {
    "pw_reset": LINK_PASSWORD_RESET,
    "pw_change": LINK_CONFIRM_PASSWORD_CHANGE, #check if needed
    "email_change_old_email": LINK_CONFIRM_EMAIL_CHANGE_OLD,
    "email_change_new_email": LINK_CONFIRM_EMAIL_CHANGE_NEW,
    "email_verification" : LINK_EMAIL_VERIFICATION,
}
URL_SUFFIX_TOKEN = "/token="

def create_verification_url(token: str, purpose: TokenPurpose) -> str:
    """
    Generates a verification URL based on the purpose and token.

    This function creates a secure verification URL by appending the provided 
    signed token and purpose to a predefined base URL. The purpose parameter 
    determines the specific action for the token (e.g., password reset, email verification).

    ----------------

    Generates a verification URL based on the purpose and token.

    **Parameters**:
        token (str): The unsigned token to include in the URL.
        purpose (TokenPurpose): An enum value representing the purpose of the verification 
                                (e.g., `TokenPurpose.PW_RESET`).

    **Returns:**
        dic: with keys:
        - "url", base link without the token ending,
        - "token_url", the url containing the the token at the end of the url,
        - "signed_token" will return the signed token.
    
    ----------------

    Example usage:
    ```python
        from app.utils.constants.enum_class import TokenPurpose

        token = "m-cLur0aKWCDLsR-D4RCoEcgAZ7SwN_kA07IaiIMfZg"
        purpose = TokenPurpose.PW_RESET
        verification_url = create_verification_url(token, purpose)
        print(verification_url["url"])
        # Output: "https://example.com//resetPassword"
        print(verification_url["token_url"])
        # Output: "https://example.com//resetPassword/token=Im0tY0x1cjBhS1dDRExzUi1ENFJDb0VjZ0FaN1N3Tl9rQTA3SWFpSU1mWmci.Z3WQMg.nBm85vaOIsATzVQskCfja412_io"
        print(verification_url["signed_token"])
        # Output: "Im0tY0x1cjBhS1dDRExzUi1ENFJDb0VjZ0FaN1N3Tl9rQTA3SWFpSU1mWmci.Z3WQMg.nBm85vaOIsATzVQskCfja412_io"
    ```
    """
    signed_token = sign_token(token, purpose)

    # Get the base URL from the dictionary
    url = purpose_url_dic.get(purpose.value)
    if not url:
        raise ValueError(f"No URL mapped for purpose '{purpose.value}'")
    
    token_url = f"{url}{URL_SUFFIX_TOKEN}{signed_token}"

    data = {
        "url": url,
        "token_url": token_url,
        "signed_token": signed_token
    }

    return data



