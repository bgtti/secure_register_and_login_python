"""
`flags.py` contains the class Flag, enums of flag colors that can be assigned to users (from the User model) or messages (from the Message model).
"""
import enum

class Flag(enum.Enum):
    """
    `Flag` is an Enum to indicate admins to check if the user is a potential spammer, attacker, or bad actor, or if a message contains improper content.

    ------------------------------------------------------------
    **Options:**
    
    - `Flag.BLUE = "blue"` #-> Default - has neither been flagged by admins not by the system.
    - `Flag.PURPLE = "purple"` #-> Message/user has been flagged by the system (possible use of profanity or possible spam): Human admin should check.
    - `Flag.YELLOW = "yellow"` #-> Indicates the user has been flagged by the system (possible html/javascript in input or potential bad actor): Human admin should check.
    - `Flag.RED = "red"` #-> Problematic action detected (multiple failed log-in attempts or similar)
    - `Flag.MAROON = "maroon"` #-> Bots (detected by system or humans)
    """
    RED = "red" 
    YELLOW = "yellow" 
    PURPLE = "purple"
    BLUE = "blue" 
    MAROON = "maroon"

FLAG_PRIORITY = {
    Flag.BLUE: 0,
    Flag.YELLOW: 1,
    Flag.PURPLE: 2,
    Flag.RED: 3,
    Flag.MAROON: 4,
}