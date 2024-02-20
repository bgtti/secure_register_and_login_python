import enum

class modelBool(enum.Enum):
    """
    modelBool is an enum used as booleans.
    modelBool.TRUE = "true"
    modelBool.FALSE = "false"  
    """
    TRUE = "true"
    FALSE = "false"

class UserAccessLevel(enum.Enum):
    """
    UserAccessLevel is an enum that indicates user access.
    UserAccessLevel.SUPER_ADMIN = "super_admin". Only one user should be a super admin. Do not use!
    UserAccessLevel.ADMIN = "admin". Only a super admin should be able to make a user an admin.
    UserAccessLevel.USER = "user". Default user access.
    """
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    USER = "user"

class UserFlag(enum.Enum):
    """
    UserFlag is an Enum to indicate admins to check if the user is a potential spammer, attacker, or bad actor.
    UserFlag.RED = "red". Multiple failed log-in attempts.
    UserFlag.YELLOW = "yellow". Indicates the user has been flagged by the system (possible html/javascript in input): Human admin should check.
    UserFlag.PURPLE = "purple". Indicates the user has been flagged by the system (possible use of profanity): Human admin should check.
    UserFlag.BLUE = "blue". Default - has neither been flagged by admins not by the system.
    """
    RED = "red" 
    YELLOW = "yellow" 
    PURPLE = "purple"
    BLUE = "blue" 