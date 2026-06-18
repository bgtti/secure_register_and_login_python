"""
`common/log_utils/get_log_level.py` contains the function get_log_level which gets a string with a log level name like "ERROR" or "WARNING" and outputs a dictionary with the level name and ID.

It uses the constant "LOG_LEVEL" (in `constants/log_levels.py`), where the log levels are defined.

-----

Currently used in log-related modules such as log_activity and log_security

"""
from app.constants.log_levels import LOG_LEVEL

def get_log_level(level_name: str) -> dict:
    """
    Parameter: key in LOG_LEVEL dictionary.

    Returns an dictionary with the level name and level id.
    If key is invalid, will default to "NOTSET".
    
    **Example**
    ```python
    level = get_log_level("WARNING")
    level -> {
            "level":"WARNING",
            "level_id": 30
            }

    level = get_log_level("hello")
    level -> {
            "level":"NOTSET",
            "level_id": 0
            }
    ```
    """
    name_upper = level_name.upper()
    res = {
        "level": name_upper if name_upper in LOG_LEVEL else "NOTSET",
        "level_id": LOG_LEVEL.get(name_upper, LOG_LEVEL["NOTSET"])
    }
    return res