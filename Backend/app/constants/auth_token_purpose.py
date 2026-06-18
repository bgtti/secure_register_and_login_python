"""
Docstring for Backend.app.constants.token_purpose
"""
# import enum

# class TokenPurpose(enum.Enum):
#     """
#     `TokenPurpose` is an Enum to indicate the reason a token is created. This is used when salting a signed token.

#     ------------------------------------------------------------
#     **Options:**
    
#     - `TokenPurpose.PW_CHANGE = "pw_change"` #-> Generated to verify a password change.
#     - `TokenPurpose.EMAIL_CHANGE_OLD_EMAIL = "email_change_old_email"` #-> Generated to verify the request to change emails from the old/current email.
#     - `TokenPurpose.EMAIL_CHANGE_NEW_EMAIL = "email_change_new_email"` #-> Generated to verify the request to change emails from the given new email.
#     - `TokenPurpose.EMAIL_VERIFICATION = "email_verification"` #-> Generated for account verification.

#     ------------------------------------------------------------
#     **Attention:**

#     Purpose definition is tightly liked to the Token model and logic surrounding token-based urls. 
#     Check both the Token db model and the token utils *(inside app/utils)* before changing constants.
#     """
#     PW_RESET = "pw_reset" 
#     PW_CHANGE = "pw_change" #check if necessary
#     EMAIL_CHANGE_OLD_EMAIL = "email_change_old_email" 
#     EMAIL_CHANGE_NEW_EMAIL = "email_change_new_email"
#     EMAIL_VERIFICATION = "email_verification" 