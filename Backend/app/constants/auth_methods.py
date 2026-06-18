"""
Docstring for Backend.app.constants.auth_methods
"""
import enum

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