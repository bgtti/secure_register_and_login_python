"""
**ABOUT THIS FILE**

auth/schemas.py contains the json schemas to validate request data in the auth routes.

------------------------
## More information

These schemas are passed in to `validate_schema` (see `app/utils/custom_decorators/json_schema_validator.py`) through the route's decorator to validate client data received in json format by comparing it to the schema rules.

"""
from app.utils.constants.account_constants import INPUT_LENGTH, NAME_PATTERN, EMAIL_PATTERN, PASSWORD_PATTERN, OTP_PATTERN
from app.utils.constants.enum_class import TokenPurpose, AuthMethods, PasswordChangeReason

# Enum to list
token_purpose_values = [purpose.value for purpose in TokenPurpose]
"""purpose can be: 'pw_reset', 'pw_change', 'email_change_old_email', 'email_change_new_email', 'email_verification'"""

login_method_values = [method.value for method in AuthMethods]
"""method can be: 'otp', 'password'"""

pw_change_reason = [reason.value for reason in PasswordChangeReason]
"""reason can be: 'reset', 'change'"""

####################################
#      REGISTRATION SCHEMAS        #
####################################

signup_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string", 
            "minLength": INPUT_LENGTH['name']['minValue'], 
            "maxLength": INPUT_LENGTH['name']['maxValue'],
            "pattern": NAME_PATTERN
            },
        "email": {
            "type": "string", 
            "minLength": INPUT_LENGTH['email']['minValue'], 
            "maxLength": INPUT_LENGTH['email']['maxValue'], 
            "pattern": EMAIL_PATTERN
            },
        "password": {
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'], 
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            "pattern": PASSWORD_PATTERN
            },
        "honeypot": {
            "type": "string", 
            "minLength":  INPUT_LENGTH['honeypot']['minValue'], 
            "maxLength": INPUT_LENGTH['honeypot']['maxValue'], 
            },
    },
    "additionalProperties": False,
    "required": ["name", "email", "password", "honeypot"]
}

delete_user_schema = {
    "type": "object",
    "title": "Warning: route used to delete a user",
    "properties": {
        "password": {
            "description": "Can only accept password.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'],
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            "pattern": PASSWORD_PATTERN
            },
        "otp": {
            "description": "Can only accept otp.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['otp']['minValue'], 
            "maxLength": INPUT_LENGTH['otp']['maxValue'], 
            "pattern": OTP_PATTERN
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            }
    },

    "additionalProperties": False,
    "required": ["password"]
}

####################################
#         SESSION SCHEMAS          #
####################################

get_otp_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string", 
            "minLength": INPUT_LENGTH['email']['minValue'], 
            "maxLength": INPUT_LENGTH['email']['maxValue'], 
            "pattern": EMAIL_PATTERN},
        "honeypot": {
            "type": "string", 
            "minLength":  INPUT_LENGTH['honeypot']['minValue'], 
            "maxLength": INPUT_LENGTH['honeypot']['maxValue'], 
            },
    },
    "additionalProperties": False,
    "required": ["email", "honeypot"]
}

login_schema = {
    "type": "object",
    "title": "Will log a user in.",
    "properties": {
        "email": {
            "description": "Email of user logging in.",
            "type": "string", 
            "minLength": INPUT_LENGTH['email']['minValue'], 
            "maxLength": INPUT_LENGTH['email']['maxValue'], 
            "pattern": EMAIL_PATTERN},
        "password": {
            "description": "Can accept passwords and otp.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'], # should be the same as OTP length
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            "pattern": PASSWORD_PATTERN
            },
        "method": {
            "description": "Whether user wants to log in with otp or password",
            "type": "string", 
            "enum": login_method_values
        },
        "is_first_factor": {
            "description": "Indicates whether this is the first (true) or second (false) authentication factor",
            "type": "boolean", 
        },
        "honeypot": {
            "description": "Designed for catching bots.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['honeypot']['minValue'], 
            "maxLength": INPUT_LENGTH['honeypot']['maxValue'], 
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. Optional.",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            }
    },
    "additionalProperties": False,
    "required": ["email", "password","method", "is_first_factor", "honeypot"]
}

####################################
#         PROFILE SCHEMAS          #
####################################

change_name_schema = {
    "type": "object",
    "title": "Will change a user's name.", 
    "properties": {
        "new_name": {
            "description": "The name the user wishes to have. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['name']['minValue'], 
            "maxLength": INPUT_LENGTH['name']['maxValue'],
            "pattern": NAME_PATTERN
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            }
    },
    "additionalProperties": False,
    "required": ["new_name"]
}

####################################
#         RECOVERY SCHEMAS         #
####################################

set_recovery_email_schema = {
    "type": "object",
    "title": "Will set user's recovery email.",
    "properties": {
        "recovery_email": {
            "description": "User's recovery email.",
            "type": "string", 
            "minLength": INPUT_LENGTH['email']['minValue'], 
            "maxLength": INPUT_LENGTH['email']['maxValue'], 
            "pattern": EMAIL_PATTERN
            },
        "password": {
            "description": "Can only accept password.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'],
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            "pattern": PASSWORD_PATTERN
            },
        "otp": {
            "description": "Can only accept otp.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['otp']['minValue'], 
            "maxLength": INPUT_LENGTH['otp']['maxValue'], 
            "pattern": OTP_PATTERN
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            }
    },

    "additionalProperties": False,
    "required": ["recovery_email", "password","otp"]
}

get_recovery_email_schema = {
    "type": "object",
    "title": "Will send the recovery email of the user.",
    "properties": {
        "password": {
            "description": "Can only accept password.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'],
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            "pattern": PASSWORD_PATTERN
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            }
    },

    "additionalProperties": False,
    "required": ["password"]
}

delete_recovery_email_schema = {
    "type": "object",
    "title": "Will delete the user's recovery email.",
    "properties": {
        "password": {
            "description": "Can only accept password.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'],
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            "pattern": PASSWORD_PATTERN
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            }
    },

    "additionalProperties": False,
    "required": ["password"]
}

####################################
#         SAFETY SCHEMAS           #
####################################

verify_account_schema = {
    "type": "object",
    "title": "Verifies user's account email address.", 
    "properties": {
        "otp": {
            "description": "Can accept otp.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['otp']['minValue'], 
            "maxLength": INPUT_LENGTH['otp']['maxValue'], 
            "pattern": OTP_PATTERN
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            }
    },
    "additionalProperties": False,
    "required": ["otp"]
}

set_mfa_schema = {
    "type": "object",
    "title": "Enables or disables multi-factor authentication for the user's account.", 
    "properties": {
        "enable_mfa": {
            "description": "Boolean to signify whether mfa should be enabled (true) or disabled (false). Otp is required only for the case of disabling mfa.",
            "type": "boolean", 
            },
        "password": {
            "description": "Can only accept password.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'],
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            "pattern": PASSWORD_PATTERN
            },
        "otp": {
            "description": "Can only accept otp.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['otp']['minValue'], 
            "maxLength": INPUT_LENGTH['otp']['maxValue'], 
            "pattern": OTP_PATTERN
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            }
    },
    "additionalProperties": False,
    "required": ["enable_mfa", "password"]
}

####################################
#    CREDENTIAL CHANGE SCHEMAS     #
####################################

reset_password_token_schema = {
    "type": "object",
    "title": "Will send a token per email so user may reset password", 
    "properties": {
        "email": {
            "description": "Email of user logging in.",
            "type": "string", 
            "minLength": INPUT_LENGTH['email']['minValue'], 
            "maxLength": INPUT_LENGTH['email']['maxValue'], 
            "pattern": EMAIL_PATTERN},
        "honeypot": {
            "description": "Designed for catching bots.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['honeypot']['minValue'], 
            "maxLength": INPUT_LENGTH['honeypot']['maxValue'], 
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. ",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            }
    },
    "additionalProperties": False,
    "required": ["email", "honeypot"]
}

change_password_schema = {
    "type": "object",
    "title": "Will change a user's password",
    "properties": {
        "new_password": {
            "description": "Can accept passwords only.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'], # should be the same as OTP length
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            "pattern": PASSWORD_PATTERN
            },
        "old_password": {
            "description": "Can accept passwords only.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'], # should be the same as OTP length
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            "pattern": PASSWORD_PATTERN
            },
        "is_first_factor": {
            "description": "Indicates whether this is the first (true) or second (false) authentication factor",
            "type": "boolean", 
        },
        "pw_change_reason": {
            "description": "The reason the user landed here: password 'reset' or 'change'",
            "type": "string", 
            "enum": pw_change_reason
        },
        "honeypot": {
            "description": "Designed for catching bots.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['honeypot']['minValue'], 
            "maxLength": INPUT_LENGTH['honeypot']['maxValue'], 
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. Optional.",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            },
        "signed_token": {
            "description": "The signed token",
            "type": "string",
            "minLength": INPUT_LENGTH['signed_token']['minValue'],
            "maxLength": INPUT_LENGTH['signed_token']['maxValue'],
            },
        "otp": {
            "description": "Can only accept otp.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['otp']['minValue'], 
            "maxLength": INPUT_LENGTH['otp']['maxValue'], 
            "pattern": OTP_PATTERN
            },
    },
    "additionalProperties": False,
    "required": ["new_password", "pw_change_reason", "is_first_factor", "honeypot"]
}

change_email_schema = {
    "type": "object",
    "title": "Will change a user's email or start the process by sending email tokens",
    "properties": {
        "new_email": {
            "description": "The email the user wants to change to.",
            "type": "string", 
            "minLength": INPUT_LENGTH['email']['minValue'], 
            "maxLength": INPUT_LENGTH['email']['maxValue'], 
            "pattern": EMAIL_PATTERN},
        "password": {
            "description": "Can accept passwords only.",
            "type": "string", 
            "minLength":  INPUT_LENGTH['password']['minValue'], # should be the same as OTP length
            "maxLength": INPUT_LENGTH['password']['maxValue'], 
            "pattern": PASSWORD_PATTERN
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. Optional.",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            },
        
    },
    "additionalProperties": False,
    "required": ["new_email", "password"]
}

change_email_token_validation_schema = {
    "type": "object",
    "title": "Will change a user's email or start the process by sending email tokens",
    "properties": {
        "signed_token": {
            "description": "The signed token",
            "type": "string",
            "minLength": INPUT_LENGTH['signed_token']['minValue'],
            "maxLength": INPUT_LENGTH['signed_token']['maxValue'],
            },
        "purpose": {
            "description": "Token purpose can be one of: TokenPurpose enum. This should answer the questions: what is this token validating? ",
            "type": "string",
            "enum": token_purpose_values,
            },
        "user_agent": {
            "description": "The HTTP User-Agent request header. Optional.",
            "type": "string", 
            "minLength": INPUT_LENGTH['user_agent']['minValue'], 
            "maxLength": INPUT_LENGTH['user_agent']['maxValue'], #TODO get regex pattern
            },
        
    },
    "additionalProperties": False,
    "required": ["signed_token", "purpose"]
}





