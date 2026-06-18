"""
`constants/log_events_security.py` contains the class SecurityEvent with enums...

Enum class with all security events that should be logged.
Use this when recording a log entry in the DB => check `models/log_security.py` for more information.

Most logs should have the level "INFO". There are comments next to the items to suggest another log level when appropriate.
Check the available log levels in the dictionary "LOG_LEVEL" available in `models/log_security.py` 


--------------

**About Security Logs**

Security logs contain events related to security and are used to track safety-relevant events in the system.
These are used to detect threats and investigate compliance issues.

--------------

**About Logs**

There are two separate logs used by this app
    1. Log activity and security: logs user actions to the db. The DB models can be found under `models/log_TYPE.py`
    2. System logs: logs all system events to a file which may be used by developers for debugging purposes. System logs are configured in the app's config file and saved in files inside the folder system_logs.


**Beware of log content**

Developers must take care of the contents being logged. Do not log plaintext passwords or sensitive information.

"""
from enum import Enum

class SecurityEvent(str, Enum):
    # Authentication
    LOGIN_SUCCESS = "LOGIN_SUCCESS" 
    LOGIN_FAILURE = "LOGIN_FAILURE" 
    LOGOUT = "LOGOUT" # NOT USED YET
    OTP_SUCCESS = "OTP_SUCCESS" 
    OTP_FAILURE = "OTP_FAILURE" 
    LOGIN_MFA_FACTOR_1_SUCCESS = "LOGIN_MFA_FACTOR_1_SUCCESS" 
    LOGIN_MFA_FACTOR_1_FAILURE = "LOGIN_MFA_FACTOR_1_FAILURE" 
    LOGIN_MFA_FACTOR_2_SUCCESS = "LOGIN_MFA_FACTOR_2_SUCCESS" # NOT USED YET
    LOGIN_MFA_FACTOR_2_FAILURE = "LOGIN_MFA_FACTOR_2_FAILURE" 
    MULTIPLE_FAILED_LOGINS = "MULTIPLE_FAILED_LOGINS" 
    POTENTIAL_BRUTE_FORCE = "POTENTIAL_BRUTE_FORCE"

    # Auth/identity verification or change
    MFA_ENABLED = "MFA_ENABLED" 
    MFA_DISABLED = "MFA_DISABLED" 
    MFA_SET_FAILURE = "MFA_SET_FAILURE"
    PASSWORD_CHANGE_SUCCESS = "PASSWORD_CHANGE_SUCCESS" 
    PASSWORD_CHANGE_FAILURE = "PASSWORD_CHANGE_FAILURE" 
    PASSWORD_RESET_REQUESTED = "PASSWORD_RESET_REQUESTED" 
    PASSWORD_RESET_REQUEST_FAILURE = "PASSWORD_RESET_REQUESTED_FAILURE" 
    PASSWORD_RESET_SUCCESS = "PASSWORD_RESET_SUCCESS" 
    PASSWORD_RESET_STEP_1 = "PASSWORD_RESET_STEP_1" 
    PASSWORD_RESET_FAILURE = "PASSWORD_RESET_FAILURE" 
    EMAIL_VERIFICATION_SENT = "EMAIL_VERIFICATION_SENT" # NOT USED YET
    EMAIL_VERIFICATION_SUCCESS = "EMAIL_VERIFICATION_SUCCESS" 
    EMAIL_VERIFICATION_FAILURE = "EMAIL_VERIFICATION_FAILURE" 
    EMAIL_CHANGE_REQUESTED = "EMAIL_CHANGE_REQUESTED" 
    EMAIL_CHANGE_REQUEST_FAILURE = "EMAIL_CHANGE_REQUEST_FAILURE" 
    EMAIL_CHANGE_SUCCESS = "EMAIL_CHANGE_SUCCESS" 
    EMAIL_CHANGE_FAILURE = "EMAIL_CHANGE_FAILURE" 

    # Account recovery
    RECOVERY_EMAIL_SET_REQUEST = "RECOVERY_EMAIL_SET_REQUEST" 
    RECOVERY_EMAIL_SET_SUCCESS = "RECOVERY_EMAIL_SET_SUCCESS" 
    RECOVERY_EMAIL_SET_FAILURE = "RECOVERY_EMAIL_SET_FAILURE" 
    RECOVERY_EMAIL_VIEW = "RECOVERY_EMAIL_VIEW" 
    RECOVERY_EMAIL_DELETION_SUCCESS = "RECOVERY_EMAIL_DELETION_SUCCESS" 
    RECOVERY_EMAIL_DELETION_FAILED = "RECOVERY_EMAIL_DELETION_FAILED" 

    # Profile name change
    USER_NAME_CHANGE_SUCCESS = "USER_NAME_CHANGE_SUCCESS" 
    USER_NAME_CHANGE_FAILURE = "USER_NAME_CHANGE_FAILURE" 

    # Account lifecycle
    ACCOUNT_CREATED = "ACCOUNT_CREATED" 
    ACCOUNT_CREATION_FAILURE = "ACCOUNT_CREATION_FAILURE"
    ACCOUNT_DELETION_REQUESTED = "ACCOUNT_DELETION_REQUESTED" # NOT USED YET
    ACCOUNT_DELETION_FAILURE = "ACCOUNT_DELETION_FAILURE"
    ACCOUNT_DELETED = "ACCOUNT_DELETED" 
    ACCOUNT_BLOCKED_STATUS_CHANGED_BY_ADMIN = "ACCOUNT_BLOCKED_STATUS_CHANGED_BY_ADMIN" 
    ACCOUNT_BLOCKED_BY_SYSTEM = "ACCOUNT_BLOCKED_BY_SYSTEM" # Suggested level: SUSPICIOUS
    ACCOUNT_UNBLOCKED = "ACCOUNT_UNBLOCKED" # NOT USED YET

    # Admin/Support personnel actions
    ADMIN_DELETED_USER = "ADMIN_DELETED_USER" # NOT USED YET
    ADMIN_VIEWED_USERS_TABLE = "ADMIN_VIEWED_USERS_TABLE" # NOT USED YET
    ADMIN_VIEWED_USER_DATA = "ADMIN_VIEWED_USER_DATA" # NOT USED YET
    ADMIN_MODIFIED_USER = "ADMIN_MODIFIED_USER" 
    ADMIN_DOWNLOADED_EXPORT = "ADMIN_DOWNLOADED_EXPORT" # Suggested level: IMPORTANT # NOT USED YET
    ADMIN_RAN_DANGEROUS_OPERATION = "ADMIN_RAN_DANGEROUS_OPERATION" # Suggested level: WARNING //==> Not in use. 

    # Authorization / roles
    USER_ROLE_CHANGED = "USER_ROLE_CHANGED" # Suggested level: IMPORTANT 

    # Access attempts
    UNAUTHORIZED_ACCESS_ATTEMPT = "UNAUTHORIZED_ACCESS_ATTEMPT" # Suggested level: WARNING //==> Not in use. # NOT USED YET
    FORBIDDEN_ACTION_ATTEMPT = "FORBIDDEN_ACTION_ATTEMPT" # Suggested level: WARNING //==> Not in use. # NOT USED YET

    # Risk / rate limiting / bot
    RATE_LIMIT_TRIGGERED = "RATE_LIMIT_TRIGGERED" # Suggested level: WARNING # NOT USED YET
    HONEYPOT_TRIGGERED = "HONEYPOT_TRIGGERED" # Suggested level: BOT 
    BOT_SUSPECTED = "BOT_SUSPECTED" # Suggested level: SUSPICIOUS # NOT USED YET

    # Suspicious patters
    MULTIPLE_FAILED_LOGINS_DIFFERENT_IPS = "MULTIPLE_FAILED_LOGINS_DIFFERENT_IPS" # Suggested level: SUSPICIOUS //==> Not in use.
    LOGIN_FROM_NEW_COUNTRY = "LOGIN_FROM_NEW_COUNTRY" # //==> Not in use.
    IMPOSSIBLE_TRAVEL = "IMPOSSIBLE_TRAVEL" # Suggested level: SUSPICIOUS //==> Not in use. - idea is to detect activity accress distant locations # NOT USED YET

    # Tokens / sessions
    TOKEN_INVALID = "TOKEN_INVALID" # //==> Not in use. # NOT USED YET
    TOKEN_EXPIRED = "TOKEN_EXPIRED" # //==> Not in use. # NOT USED YET
    TOKEN_SIGNATURE_INVALID = "TOKEN_SIGNATURE_INVALID" # //==> Not in use. # NOT USED YET
    SESSION_REVOKED = "SESSION_REVOKED" # //==> Not in use. # NOT USED YET

    # Undefined/NOTSET (due to error in function parameter) => must be investigated when spottet
    UNKNOWN_EVENT = "UNKNOWN_EVENT" 