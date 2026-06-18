"""
`constants/log_levels.py` contains the dictionary LOG_LEVEL, which defines all log categories and their respective IDs.

**IMPORTANT**
Use a helper function to acquire the correct log level name and ID from a string.
This exists in `common/log_utils/get_log_level`.

--------------

**About log levels**

Logs that are marked "Critical", "Error", "Warning", or "Suspiscious" should be presented to admins or devs to verify.

Note that logs with "Critical" or "Error" levels might indicate the system or databse is down. As such, they might not get logged in the database or this app might not be up and available to make decision makers aware of the problem.

It is important, therefore, to log such events using another method.

"""
LOG_LEVEL = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30, # system or account might be under attack
    "SUSPICIOUS":25, # a relevant decision maker should check
    "IMPORTANT": 21, # perhaps super admin would want to be informed of such actions
    "INFO": 20,
    "BOT":15, # for confirmed bots (eg: caught in honeypot) 
    "DEBUG": 10,
    "NOTSET": 0
}
"""Log level dictionary: CRITICAL, ERROR, WARNING, SUSPICIOUS, INFO, BOT, DEBUG, NOTSET"""

