"""
**ABOUT THIS FILE**

group_id_creation.py contains a utility function that can be used to generate a group_id for the Token db model. 

--------------------
**Content**

The function:
- *get_group_id* gets the user's id and adds it to form a unique string that can be used as group_id

"""
from datetime import datetime, timezone

def get_group_id(user_id):
    """
    get_group_id(user_id: int) --> str

    ---------
    If creating tokens that should be related, use this function to get a 'unique enough' string to be used as the token's group_id.

    ---------
    **How it works:** the uder's id is combined with a timestamp.

    **Example:** `get_group_id(42) # --> will return '42-1701112540'`
    
    """
    # Current timestamp (to the second)
    timestamp = int(datetime.now(tz=timezone.utc).timestamp())
    return f"{user_id}-{timestamp}" 