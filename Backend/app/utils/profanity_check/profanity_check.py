from app.utils.profanity_check.profanity_words import PROFANITY_WORD_LIST

def has_profanity(user_input):
    """
    has_profanity(user_input: str) -> bool
    ---------------------------------------
    Returns:
        False if user_input does not include any word in the profanity word list.
        True if user_input includes any word in the profanity word list.
    ---------------------------------------
    Important:
        The profanity word list also includes common words, so the outcome of this function should not be used to block a user, but rather flag the user - and an admin should review the input and decide whether the user should be blocked or not. Context is important. Example: the letters "nig" can be found in the word "Nigeria" or in offensive slang.
    --------------------------------------
    Example usage:
    word_to_check = has_profanity("the movie How to Murder Your Husband was not funny") # word_to_check == True

    word_to_check = has_profanity("the movie HTMMYH was not funny") # word_to_check == False
    """
    if any(profanity in user_input for profanity in PROFANITY_WORD_LIST):
        return True

    return False