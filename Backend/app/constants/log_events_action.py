from enum import Enum

class ActionEvent(str, Enum):
    # Profile
    USER_PROFILE_UPDATED = "USER_PROFILE_UPDATED"

    # Messages
    MESSAGE_SENT = "MESSAGE_SENT"
    MESSAGE_DELETED = "MESSAGE_DELETED"

    # Preferences
    SET_MAILING_LIST = "SET_MAILING_LIST"
    SET_NIGHT_MODE = "SET_NIGHT_MODE"

    # Unknown
    UNKNOWN_EVENT = "UNKNOWN_EVENT"

    # Add whatever else your system does that is not covered in SecurityEvents...