import enum

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

class SecretKeyPurpose(enum.Enum):
    """
    `SecretKeyPurpose` is an Enum to indicate the purpose for which a SecretKey was created.
    Currently secret keys are used to validate a request to change password or email.

    ------------------------------------------------------------
    **Options:**
    
    - `EMAIL_CHANGE = "email_change"` 
    - `PASSWORD_CHANGE = "password_change"`
    """
    EMAIL_CHANGE = "email_change" 
    PASSWORD_CHANGE = "password_change" 