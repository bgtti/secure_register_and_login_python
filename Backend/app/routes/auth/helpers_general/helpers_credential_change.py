# Python/Flask libraries
import logging

# Extensions
from app.extensions.extensions import db

# Database models
from app.models.token import Token

# Utilities
from app.utils.constants.enum_class import TokenPurpose
from app.utils.token_utils.sign_and_verify import verify_signed_token

def validate_and_verify_signed_token(signed_token: str, token_purpose: TokenPurpose, function_name: str, invalidate_token: bool) -> dict:
    """
    Retrieves and validates a token from the database.

    This function verifies a signed token, ensures it matches the intended purpose, and validates it 
    against the database for expiration or validity. 
    Should the token be marked as used, pass True to invalidate_token parameter. 

    ---------------------
    **Parameters:**

        signed_token (str): The signed token string to validate and verify.
        token_purpose (TokenPurpose): The intended purpose of the token (e.g., PW_RESET).
        function_name (str): Name of the calling function.
        invalidate_token (bool): invalidates token after checking validity
    
    **Returns:**
        A dictionary containing:
            - status (int): 200 if successful, other values if failed.
            - message (str): Error message if validation fails, empty string otherwise.
            - token (Token): The token object if successfully retrieved and validated, None otherwise.
    
    ---------------------
    **Example usage:**

    ```python
    signed_token = Ikl3V0JaSlV3MmhocEsyNkNrV0J0S2VhSlJqVDdqaWk2VFFhRXRLYmZkXzAi.Z3WSBA.cJQmqDVQDjMeMj92B-RRzkD4JtM
    token_purpose = TokenPurpose.PW_RESET
    function_name = "change_password"

    token = validate_and_verify_signed_token(signed_token,token_purpose, function_name)

    print(token["status"]) # Returns: 200
    print(token["message"]) # Returns: ""
    print(token["token"]) # Returns: Token object
    ```
    """

    response = {
        "status": 200,
        "message": "",
        "token": None
    }

    # Check if token_purpose is valid
    if not isinstance(token_purpose, TokenPurpose):
        raise ValueError(f"Invalid token purpose: {token_purpose}. Must be a member of TokenPurpose.")

    token = verify_signed_token(signed_token, token_purpose)
        
    if not token:
        logging.info(f"Invalid or expired token could not be validated in function {function_name}.")
        response["status"] = 400
        response["message"] = "Error: token may be expired or invalid."
        return response

    # Fetch the token from the database
    try:
        the_token =Token.query.filter_by(token=token).first()
        if not the_token:
            response["status"] = 404
            response["message"] = "Error: Token not found in the database."
            logging.info(f"Error: token not found in function {function_name}.")
            return response
    except Exception as e:
        response["status"] = 500
        response["message"] = "Database error occurred."
        logging.error(f"Database error while fetching token in function {function_name}. Error: {e}")
        return response

    # Validate token
    try:
        if the_token.validate_token(invalidate_token):
            db.session.commit()
        else:
            response["status"] = 400
            response["message"] = "Error: token may be expired or invalid."
            logging.info(f"Token validation failed in function {function_name}.")
            return response
    except Exception as e:
        db.session.rollback()
        response["status"] = 500
        response["message"] = "Error: database error occurred during token validation."
        logging.error(f"Database error while validating token in function {function_name}. Error: {e}")
        return response
    
    # Return token
    response["token"] = the_token
    return response

