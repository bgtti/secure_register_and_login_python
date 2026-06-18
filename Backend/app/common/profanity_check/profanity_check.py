from app.common.profanity_check.profanity_words import PROFANITY_WORD_LIST

def has_profanity(user_input: str) -> bool:
    """
    Checks string against a profanity word  list.
    Return True if one of the words is included in the string, False otherwise.

    Important:
        The profanity word list also includes common words, so the outcome of this function should not be used to block a user, but rather flag the user - and an admin should review the input and decide whether the user should be blocked or not. Context is important. Example: the letters "nig" can be found in the word "Nigeria" or in offensive slang.
    
    Example usage:
    ```python
    word_to_check = has_profanity("the movie How to Murder Your Husband was not funny") # => True
    word_to_check = has_profanity("the movie HTMMYH was not funny") # => False
    ```
    """
    if any(profanity in user_input for profanity in PROFANITY_WORD_LIST):
        return True

    return False