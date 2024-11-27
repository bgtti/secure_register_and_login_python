"""
**ABOUT THIS FILE**

**Content**: Token database model. 

--------------------
**What the model is used for**

Create a token when there is a need to validate a request, such as a password change.
A Token is linked to a user, and it's creation is expected to have a purpose (like a password change verification).

--------------------
**Token usage flow: example**

1) The user request a password change.
2) Create a token with the purpose "pw_change" *(using the appropriate enum --> check app/utils/constants)*
3) Pass the token and the purpose for the token creation to sign_token() *(--> check app/utils/token_utils)* to get the signed token 
4) Send the signed token to the user wrapped in a url
5) User will click the url and the front end will send a request with the signed token
6) Get the signed token provided by te client (which should contain information about its purpose) and feed it to verify_signed_token() *(--> check app/utils/token_utils)*
7) If a token is returned from the verification, check for its existence in the database

Extra step: if the usage flow was that of an email change, create two tokens with the same group_id. Use the

*uffff, this sounds overly complicated...* --> yes, but this flow will make it very difficult for bad actors to tamper with the token, and token are only used for... well, authenticating a credential change, so the effort may be worth it.

--------------------
**Important considerations**

- Delete a token after it's been used.
- If an email change request needs validation, a second token will be needed (to validate both new and old email addresses). The group_id should be used for this purpose. Check the utils folder for token-related utils and use the group_id creation function to assign the same group_id to both newly created tokens.
- **DO NOT** send a token as it is in the db to the client! Tokens should be signed before sending. Check the utils directory for token-related utils where you should find the signing and verification functions.

--------------------
**More info**

Check out the base logic behind all of this: https://stackoverflow.com/questions/23039734/flask-login-password-reset

--------------------
**TODO: missing token functionality**

Needs a script to delete old tokens to keep the db clean. Perhaps run it once per month or so.
"""
import secrets
from sqlalchemy.orm import validates
from datetime import datetime, timedelta, timezone
from flask_login import UserMixin
from app.utils.constants.enum_class import TokenPurpose
from app.extensions.extensions import db
from app.utils.constants.enum_class import modelBool

# TODO consider keeping functions inside the models itself and using the model boolean:
# class Token(db.Model):
#     __tablename__ = 'tokens'
#     ...
#     token = db.Column(db.String(200), nullable=False, unique=True, default=lambda: Token.get_token()) <--- *
#     ....
#     token_verified = db.Column(db.Boolean, default=False, nullable=False) <--- *
#     ...
#     @staticmethod <--- *
#     def get_token():
#         """
#         Returns a cryptographically secure random token. 
#         """
#         return secrets.token_urlsafe(32)

def get_token():
    """
    Returns a cryptographically secure random token. 
    Uses secrets.token_urlsafe with 32 bytes given. Each byte resulting in aprox 1.3 characters, so:  about 43 characters long.
    """
    return secrets.token_urlsafe(32)

def expiration_date():
    """
    Returns a datetime object of datetime one hour from 'now'.
    """
    return datetime.now(timezone.utc) + timedelta(hours=1)

class Token(db.Model, UserMixin):
    """
    Token Database Model
    --------------------------------------------------------------
    **Purpose:**
    This model represents a token used for authentication-related functionality or actions.
    Tokens are used for various purposes, including password resets, email changes, or
    account verification. Each token is associated with a user and contains metadata
    such as its purpose, creation time, expiration date, and usage status.

    **Attributes:**
    - **id (int):** Primary key, uniquely identifies each token.
    - **token (str):** A unique cryptographically secure random string, used to authenticate
      or authorize an action.
    - **purpose (TokenPurpose):** Enum defining the reason this token was generated
      (e.g., password reset, email change).
    - **token_verified (modelBool):** Enum indicating whether the token has been used or verified.
      Defaults to `modelBool.FALSE`. 
    - **created_at (datetime):** The timestamp of when the token was created, defaults to
      the current UTC time.
    - **expiry_date (datetime):** The timestamp of when the token will expire, calculated using
      the `expiration_date` function (default is 1hr).
    - **ip_address (str, optional):** IP address of the request that generated the token.
    - **user_agent (str, optional):** Information about the device or browser that generated the token.
    - **group_id (str, optional):** A shared identifier for related tokens, such as for email
      change workflows involving old and new email verification tokens.
    - **user_id (int):** Foreign key linking the token to a specific user in the `user` table.

    **Methods:**
    - `__init__`: Initializes a new Token object with optional IP address, user agent, and group ID.
    - `__repr__`: Provides a string representation of the token for debugging or logging purposes.
    - `validate_group_id`: Ensures that `group_id` is not `None` when the token's purpose is
      `TokenPurpose.EMAIL_CHANGE_NEW_EMAIL` or `TokenPurpose.EMAIL_CHANGE_OLD_EMAIL`.
    - `validate_token`: Validates the token by checking its expiration status and whether it
      has already been used. If valid, it marks the token as verified.

    **Usage:**
    This model is used to generate, store, and validate tokens required for authentication-related
    processes. Tokens are unique, have an expiration date, and can only be used once for their
    intended purpose.
    For signing and verification, refer to the `app/utils/token_utils.py` file.

    **Examples:**
    - Adding a new token to the database:
      ```python
      from app.models.token import Token

      # Create a token for password reset
      new_token = Token(
          user_id=10,
          purpose=TokenPurpose.PASSWORD_RESET,
          ip_address="192.168.1.1",
          user_agent="Mozilla/5.0"
      )
      db.session.add(new_token)
      db.session.commit()
      ```

    - Querying for related tokens using `group_id`:
      ```python
      # Fetch all tokens related to a specific group_id
      related_tokens = Token.query.filter_by(group_id="shared_group_id").all()

      for token in related_tokens:
          print(f"Token ID: {token.id}, Purpose: {token.purpose.value}, Verified: {token.token_verified}")
      ```
    
    """
    __tablename__ = "token"
    # main characteristics
    id = db.Column(db.Integer, primary_key=True, unique=True)
    token = db.Column(db.String(45), unique=True, default=get_token, nullable=False)
    purpose = db.Column(db.Enum(TokenPurpose), nullable=False) # TODO consider enum definition in db
    # token status
    token_verified = db.Column(db.Enum(modelBool), default=modelBool.FALSE, nullable=False) # user used the token 
    # token creation extra info
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    expiry_date = db.Column(db.DateTime, default=expiration_date, nullable=False)
    ip_address = db.Column(db.String(250), nullable=True) # ip address of the request
    user_agent = db.Column(db.String(255), nullable=True) # some device information
    # token belonging info
    group_id = db.Column(db.String(20), nullable=True)  # Shared ID for related tokens (e.g., email change pair)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, user_id, purpose, ip_address=None, user_agent=None, group_id=None, **kwargs):
        self.user_id = user_id
        self.purpose = purpose
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.group_id = group_id
    
    def __repr__(self):
        return f"<Token: {self.id} created>"
    
    @validates('group_id')
    def validate_group_id(self, key, value):
        """Validate group_id for email change purposes."""
        if self.purpose in {TokenPurpose.EMAIL_CHANGE_NEW_EMAIL, TokenPurpose.EMAIL_CHANGE_OLD_EMAIL} and not value:
            raise ValueError(f"group_id is required for purpose '{self.purpose.value}' but was not provided.")
        return value
    
    
    def validate_token(self):
        """
        validate_token()-> bool
        -----------------------------
        Will return true if the token is valid and false otherwise.
        Will mark the token as used by setting token_verified to true.
        """
        now = datetime.now(timezone.utc)
        token_is_valid = self.created_at < now <= self.expiry_date
        token_was_not_used = self.token_verified == modelBool.FALSE

        if token_is_valid and token_was_not_used:
            self.token_verified = modelBool.TRUE
            return True
        else:
            return False
    
    # def validate_email_token(self):
    #     """
    #     validate_email_token()-> bool
    #     -----------------------------
    #     Will return true if the new_email_token is valid and false otherwise.
    #     Will mark the new_email_token as used by setting new_email_token_verified to true.
    #     """
    #     now = datetime.now(timezone.utc)
    #     token_is_valid = self.created_at < now <= self.expiry_date
    #     token_was_not_used = self.new_email_token_verified == modelBool.FALSE

    #     if token_is_valid and token_was_not_used:
    #         self.new_email_token_verified = modelBool.TRUE
    #         return True
    #     else:
    #         return False
    
    # def user_may_change_email(self):
    #     """
    #     user_may_change_email()-> bool
    #     -----------------------------
    #     Will return true if both tokens were verified and they are still valid.
    #     Will return false otherwise.
    #     """
    #     now = datetime.now(timezone.utc)
    #     token_is_valid = self.created_at < now <= self.expiry_date
    #     old_email_verified = self.token_verified == modelBool.TRUE
    #     new_email_verified = self.token_verified == modelBool.TRUE

    #     if token_is_valid and old_email_verified and new_email_verified:
    #         return True
    #     else:
    #         return False





# TODO RUN PERIODICALLY with celery, apsscheduler, or a cron job:
# from flask import current_app

# def cleanup_expired_tokens():
#     with current_app.app_context():
#         expired_tokens = ValidationToken.query.filter(ValidationToken.expires_at < datetime.utcnow()).all()
#         for token in expired_tokens:
#             db.session.delete(token)
#         db.session.commit()