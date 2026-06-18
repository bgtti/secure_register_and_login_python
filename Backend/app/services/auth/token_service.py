"""
TODO check if token services are still necessary
"""
# # Python/Flask libraries
# import logging
# from datetime import datetime, timedelta, timezone

# # Extensions
# from app.extensions.extensions import db, limiter, flask_bcrypt

# # Models
# from app.models.user import User
# from app.models.token import Token

# # Constants
# from app.constants.auth_token_purpose import TokenPurpose
# from app.constants.auth_password_change import PasswordChangeReason

# # Utilities
# from app.common.token_utils.sign_and_verify import verify_signed_token

# # Other services
# from app.services.auth.user_block_service import svc_check_if_user_blocked

# def svc_create_token(user: User, token_purpose: TokenPurpose | str, ip_address: str, user_agent: str):
#     """
#     Function in `services/auth/token_service.py`.
#     Used to create a token that can be used for credential change.

#     **This function does the following:**
#     - Checks if a user is blocked from logging in, either temporarily due to failed login attempts.
#     or permanently by an admin (and returns 403 log code if so).
#     - Creates a token in the DB and commits the changes.
#     - Returns the created token along with useful information for logging or decision making.
#     - Checks if user is Super Admin (and returns 202 log code if so, but token will be created in this case as well).

#     **This function does not do the following:**
#     - It will not create the token url or sign the token (use create_verification_url for this)
#     - It will not send any emails


#     Args:
#         user (User): The user object being checked.
#         token_purpose (TokenPurpose | str): A TokenPurpose enum member or one of its valid values (example: TokenPurpose.PW_RESET or just "pw_reset").
#         ip_address (str): the client's ip address
#         user_agent (str): user agent sending the request

#     Returns:
#         dict: A dictionary with the following keys:
        
#             - "success" (bool): True if token was created, otherwise False.
#             - "token" (str): The token saved to the DB (as string).
#             - "is_admin_blocked" (bool): Whether user was blocked by admin (True) or not (False)
#             - "is_login_blocked" (bool): Whether user was blocked by the system for too many login attempts (True) or not (False)
#             - "wait_time" (int): An integer indicating the time (in minutes or seconds) the client has to wait until the block is lifted (eg: `10` or `52`).
#             - "wait_time_measure" (str): Either "minute", "minutes", "second", or "seconds"
#             - "is_super_admin" (bool): Whether user is super admin (True) or not (False).
#             - "log_code" (int): An http-logic log code to be used with logging function.
#             - "log_text" (str): A log message. To be used internally only.
    
#     Example:
#     ```
#     user = get_user_or_none(email, "reset_password_token")
#     token_data = svc_create_token(user, TokenPurpose.PW_RESET, "192.168.0.1", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

#     token_data --> {
#         "success": True,
#         "token":"Drmhze6EPcv0fN_81Bj-nADrmhze6EPcv0fN_81Bj-nA",
#         "is_admin_blocked": False,
#         "is_login_blocked": False,
#         "wait_time": None,
#         "wait_time_measure": None,
#         "is_super_admin": False,
#         "log_code": 200,
#         "log_text": "",
#     }
#     ```
#     """
#     # Prepare response
#     res = {
#         "success": False,
#         "token": "",
#         "is_admin_blocked": False,
#         "is_login_blocked": False,
#         "wait_time": None,
#         "wait_time_measure": None,
#         "is_super_admin": False,
#         "log_code": 500,
#         "log_text": "",
#     }
#     # Check enum
#     try:
#         token_purpose = TokenPurpose(token_purpose)
#     except ValueError:
#         raise ValueError("Invalid token purpose: must be a TokenPurpose or valid TokenPurpose value.")
    
#     # Check if user was sent in correctly in request
#     if not user or not isinstance(user, User) or not user.id:
#         res["log_code"] = 501
#         res["log_text"] = f"Service request sent without user email or id. User could not be identified."
#         logging.error(f"svc_create_token found no user. Token creation failed.")
#         return res
    
#     # Check if user is blocked
#     blocked_status = svc_check_if_user_blocked(user)
#     if blocked_status["blocked"]:
#         res["log_code"] = 403
#         if blocked_status["temporary_block"] is False: # means user was blocked by admin
#             res["is_admin_blocked"] = True
#             res["log_text"] = "User is admin blocked."
#         else:
#             # NOTE:
#             # Consider allowing password recovery for temporarily blocked users: too many failed log ins may indicate user forgot password.
#             # Be purpose specific: allow reset for PW_RESET cases
#             res["is_login_blocked"] = True
#             res["log_text"] = "User is temporarily blocked due to too many failed login attempts."
#             res["wait_time"] = blocked_status["wait_time"]
#             res["wait_time_measure"] = blocked_status["wait_time_measure"]
#         return res

#     # Create token
#     try:
#         token = Token(user_id=user.id, purpose=token_purpose, ip_address=ip_address, user_agent=user_agent) 
#         db.session.add(token)
#         db.session.commit()

#     except Exception as e:
#         db.session.rollback()
#         logging.error(f"Token creation failed. Error: {e}")
#         res["log_text"] = f"Token creation failed. Error: {e}"
#         return res
    
#     res["success"] = True
#     res["token"] = token.token

#     # Check if is super admin
#     if user.role.access_level == "super_admin":
#         res["is_super_admin"] = True
#         res["log_code"] = 201
#         res["log_text"] = f"Super admin requested token creation for purpose={token_purpose.value}."
#         logging.warning(f"Super admin requested token creation for purpose={token_purpose.value}.")
#         return res
    
#     # Creation successful
#     res["log_code"] = 200
#     res["log_text"] = f"Token created successfully for user id={user.id}"

#     return res

# def svc_validate_token(token: Token, mark_as_used: bool = False) -> bool:
#     """
#         Function in `services/auth/token_service.py`.

#         This function checks the token from the DB: whether is it valid based on its creation and expiration dates,
#         and whether it has been used. Optionally, the token can be marked as 'used'.

#         If `mark_as_used` is True: will set token.token_verified = True only. This function does not commit changes to the database.

#         Returns:
#             bool: True if the token is valid, False otherwise. Also returns False if marking the token as used fails.

#         Note: 
#         - Ensure this token is marked as 'used' when appropriate (e.g., after successful MFA).
#         - Ensure db.session.commit() is called by the caller if mark_as_used is set to True
#     """
#     now = datetime.now(timezone.utc)

#     if not token or not isinstance(token, Token):
#         logging.error("Invalid token passed to svc_validate_token.")
#         return False

#     # Perform comparison using aware datetimes
#     token_is_valid = token.created_at < now <= token.expiry_date
#     token_was_not_used = token.token_verified == False

#     if token_is_valid and token_was_not_used:
#         if mark_as_used:
#             token.token_verified = True
            
#         return True
#     else:
#         return False


# def svc_validate_and_verify_signed_token(signed_token: str, token_purpose: TokenPurpose | str, function_name: str, invalidate_token: bool) -> dict:
#     """
#     Function in `services/auth/token_service.py`.
#     Used to verify and validate a token stored in the DB (ensures it matches the intended purpose, and validates it 
#     against the database for expiration or validity). Should the token be marked as used, pass True to invalidate_token parameter. Changes will be committed to the DB.

#     **This function does the following:**
#     - Verifies the signed token and decodes it using utility func `verify_signed_token`
#     - Fetches token from DB
#     - Validates token using service func `validate_token`
#     - Optionally invalidates token marking it as used in the db and committing changes

#     ---------------------
#     **Parameters:**

#         signed_token (str): The signed token string to validate and verify.
#         token_purpose (TokenPurpose): The intended purpose of the token (e.g., PW_RESET). May be str value or enum.
#         function_name (str): Name of the calling function.
#         invalidate_token (bool): invalidates token after checking validity
    
#     **Returns:**
#         A dictionary containing:
#             - status (int): 200 if successful, other values if failed, to be used for logging.
#             - message (str): Error message if validation fails, empty string otherwise, to be used for logging.
#             - token (Token): The token object if successfully retrieved and validated, None otherwise.
    
#     ---------------------
#     **Example usage:**

#     ```python
#     signed_token = Ikl3V0JaSlV3MmhocEsyNkNrV0J0S2VhSlJqVDdqaWk2VFFhRXRLYmZkXzAi.Z3WSBA.cJQmqDVQDjMeMj92B-RRzkD4JtM
#     token_purpose = TokenPurpose.PW_RESET
#     function_name = "change_password"
#     invalidate_token = True

#     token = svc_validate_and_verify_signed_token(signed_token,token_purpose, function_name, invalidate_token)

#     print(token["status"]) # Returns: 200
#     print(token["message"]) # Returns: ""
#     print(token["token"]) # Returns: Token object
#     ```
#     """

#     response = {
#         "status": 200,
#         "message": "",
#         "token": None
#     }

#     # Check if token_purpose is valid
#     try:
#         token_purpose = TokenPurpose(token_purpose)
#     except ValueError:
#         raise ValueError("Invalid token purpose. Must be a TokenPurpose or a valid TokenPurpose value.")

#     # Validate token (check if it is real and get decoded value)
#     verified_token = verify_signed_token(signed_token, token_purpose)
        
#     if not verified_token:
#         logging.info(f"Invalid or expired token could not be validated in function {function_name}.")
#         response["status"] = 400
#         response["message"] = "Error: token may be expired or invalid."
#         return response

#     # Fetch the token from the database
#     try:
#         db_token = Token.query.filter_by(token=verified_token).first()
#         if not db_token:
#             response["status"] = 404
#             response["message"] = "Error: Token not found in the database."
#             logging.info(f"Error: token not found in function {function_name}.")
#             return response
#     except Exception as e:
#         response["status"] = 500
#         response["message"] = "Database error occurred."
#         logging.error(f"Database error while fetching token in function {function_name}. Error: {e}")
#         return response

#     # Validate token
#     token_is_valid = svc_validate_token(db_token, invalidate_token)

#     if not token_is_valid:
#         response["status"] = 400
#         response["message"] = "Error: token may be expired or invalid."
#         logging.info(f"Token validation failed in function {function_name}.")
#         return response

#     if invalidate_token:
#         try:
#             db.session.commit()
#         except Exception as e:
#             db.session.rollback()
#             response["status"] = 500
#             response["message"] = "Error: database error occurred during token validation."
#             logging.error(f"Database error while validating token in function {function_name}. Error: {e}")
#             return response
    
#     # Return token
#     response["token"] = db_token
#     return response