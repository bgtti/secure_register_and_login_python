"""
Docstring for Backend.app.constants.auth_password_change
"""
import enum

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