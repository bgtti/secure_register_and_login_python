import enum

#TODO if shared enums between front and backend, then centralize the source of truth instead of repeting things
#TODO change name of "UserFlag" to just "Flag"

class modelBool(enum.Enum):
    """
    `modelBool` is an enum used as booleans.

    ------------------------------------------------------------
    **Options:**
    
    - `modelBool.TRUE = "true"` 
    - `modelBool.FALSE = "false" ` 
    """
    TRUE = "true"
    FALSE = "false"

class UserAccessLevel(enum.Enum):
    """
    `UserAccessLevel` is an enum that indicates user access.

    ------------------------------------------------------------
    **Options:**
    
    - `UserAccessLevel.SUPER_ADMIN = "super_admin"` #-> Only one user should be a super admin. Do not use!
    - `UserAccessLevel.ADMIN = "admin"` #-> Only a super admin should be able to make a user an admin.
    - `UserAccessLevel.USER = "user"` #-> Default user access.
    """
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    USER = "user"

class UserFlag(enum.Enum):
    """
    `UserFlag` is an Enum to indicate admins to check if the user is a potential spammer, attacker, or bad actor.

    ------------------------------------------------------------
    **Options:**
    
    - `UserFlag.BLUE = "blue"` #-> Default - has neither been flagged by admins not by the system.
    - `UserFlag.PURPLE = "purple"` #-> Indicates the user has been flagged by the system (possible use of profanity): Human admin should check.
    - `UserFlag.YELLOW = "yellow"` #-> Indicates the user has been flagged by the system (possible html/javascript in input): Human admin should check.
    - `UserFlag.RED = "red"` #-> Multiple failed log-in attempts.
    """
    RED = "red" 
    YELLOW = "yellow" 
    PURPLE = "purple"
    BLUE = "blue" 

class TokenPurpose(enum.Enum):
    """
    `TokenPurpose` is an Enum to indicate the reason a token is created. This is used when salting a signed token.

    ------------------------------------------------------------
    **Options:**
    
    - `TokenPurpose.PW_CHANGE = "pw_change"` #-> Generated to verify a password change.
    - `TokenPurpose.EMAIL_CHANGE_OLD_EMAIL = "email_change_old_email"` #-> Generated to verify the request to change emails from the old/current email.
    - `TokenPurpose.EMAIL_CHANGE_NEW_EMAIL = "email_change_new_email"` #-> Generated to verify the request to change emails from the given new email.
    - `TokenPurpose.EMAIL_VERIFICATION = "email_verification"` #-> Generated for account verification.

    ------------------------------------------------------------
    **Attention:**

    Purpose definition is tightly liked to the Token model and logic surrounding token-based urls. 
    Check both the Token db model and the token utils *(inside app/utils)* before changing constants.
    """
    PW_RESET = "pw_reset" 
    PW_CHANGE = "pw_change" #check if necessary
    EMAIL_CHANGE_OLD_EMAIL = "email_change_old_email" 
    EMAIL_CHANGE_NEW_EMAIL = "email_change_new_email"
    EMAIL_VERIFICATION = "email_verification" 

class AuthMethods(enum.Enum):
    """
    `AuthMethods` is an Enum to indicate the method a user chooses to authenticate.
    Login should allow OTP or password.
    Credential changes may allow for token.

    ------------------------------------------------------------
    **Options:**
    
    - `AuthMethods.PASSWORD = "password"` 
    - `AuthMethods.OTP = "otp"` .

    ------------------------------------------------------------
    **Purpose:**

    A user can choose to log in with an otp or with a one-time password.
    """
    PASSWORD = "password" 
    OTP = "otp" 
    TOKEN = "token" 


class PasswordChangeReason(enum.Enum):
    """
    `PasswordChangeReason` is an Enum to indicate the reason for a password change.

    ------------------------------------------------------------
    **Options:**
    
    - `PasswordChangeReason.RESET = "reset"` for when a user forgets the password
    - `PasswordChangeReason.CHANGE = "change"` for when a user wants to change the password

    ------------------------------------------------------------
    **Purpose:**

    Each reason will require a different method to change a password.
    """
    RESET = "reset" 
    CHANGE = "change"  