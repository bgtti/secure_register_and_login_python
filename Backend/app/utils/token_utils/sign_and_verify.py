"""
**ABOUT THIS FILE**

sign_and_verify.py contains utility functions concearned with the signing and validating tokens created using the Token db model. 

--------------------
**Content**

The functions:
- *sign_token* will wrap the token in a unique signature. This is a required step before serving any token to a client
- *verify_signed_token* will check if a sign token is valid. It will returned to unsigned token so it may be checked against the database.

"""
import logging
from itsdangerous import SignatureExpired, BadSignature
from app.utils.constants.enum_class import TokenPurpose
from app.extensions.extensions import serializer

def sign_token(token, purpose):
    """
    **sign_token(token: str, purpose: enum) --> str**

    ---------------------
    Signs and timestams token and returns the signed token.
    Token will be salted with the given purpose.
    A token should only be sent [eg to a user] after it has been signed. 

    ---------------------
    **Parameters:**

        signed (str): The token to sign.
        purpose (enum class TokenPurpose): The purpose of the token (will be used to salt it).
    
    **Returns:**

        str: The signed and timestamped token.
    """
    if purpose not in TokenPurpose.__members__.values():
        logging.error(f"Failed to provide a valid purpose to the sign_token function. Purpose must e a member of the enum class TokenPurpose defined in the util package constants.")
        raise ValueError(f"Invalid token purpose: {purpose.value}")
    signed_token = serializer.dumps(token, salt=purpose.value)
    return signed_token #TODO: test to make sure this does not exceed 200 characters

def verify_signed_token(signed_token, purpose, max_age_in_sec = 3600):
    """
    **verify_signed_token(signed_token: str, purpose: enum | str,  max_age_in_sec: int=3600) --> str | None**

    Verifies a signed token and validates its purpose and expiration.

    ---------------------
    **Parameters:**

        signed_token (str): The signed token to verify.
        purpose (enum class TokenPurpose or its string value): The purpose of the token (used as a salt).
        max_age_in_sec (int): Maximum age of the token in seconds (default: 3600, 1 hr).
    
    Returns:
        str or None: The decoded token data if valid; otherwise None.

    Example:

    """
    # if purpose is passed as an enum, it should be translated to string
    purpose_str = purpose if isinstance(purpose, str) else purpose.value

    if purpose_str not in [member.value for member in TokenPurpose]:
        logging.error(f"Failed to provide a valid purpose to the verify_signed_token function. Purpose must e a member of the enum class TokenPurpose defined in the util package constants.")
        raise ValueError(f"Invalid token purpose: {purpose}")

    token_preview = "Signed_token(first 8 digs)= " + signed_token[:8] + "..." if signed_token else "None"
    try:
        token= serializer.loads(signed_token, salt=purpose_str, max_age=max_age_in_sec)
        return token #compare this value to the one in the db to see if matches
    except SignatureExpired:
        logging.info(f"Token verification failed: token has expired. {token_preview}")
    except BadSignature:
        logging.warning(f"Token verification failed: token signature is invalid or has been tampered. {token_preview}")
    except Exception as e:
        logging.error(f"Token verification failed for {token_preview}. Error: {e}")
    return None