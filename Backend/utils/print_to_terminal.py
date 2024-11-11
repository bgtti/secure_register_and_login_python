"""
**ABOUT THIS FILE**

print_to_terminal.py contains the function **print_to_terminal** which prints messages to the terminal in different colours. Can be helpful to warn of errors during development.

"""

from colorama import Fore

def print_to_terminal(message, color="BLUE"):
    """
    print_to_terminal(message: str, color: str = "BLUE") -> None
    ------------------------------------------------------------

    Takes a message (and, optionally, a colour) and prints it to the terminal in the given colour.
    Meant to be colored and serve as a warning.

    ------------------------------------------------------------

    **Arguments:**
        Message as a string and, optionally, the colour as used in colorama.

    **Colour options:**
        "BLUE", "CYAN", "MAGENTA", "RED", "GREEN", "YELLOW", "WHITE".

    **Returns:**
        The message printed to the terminal in the chosen colour.
    ------------------------------------------------------------
    **Example usage:**

        `print_to_terminal("hello", "GREEN") # -> prints message in green`
        `print_to_terminal("hello console") # -> prints message in blue once`
    """
    colors = {
        "BLUE": Fore.BLUE,
        "CYAN": Fore.CYAN,
        "MAGENTA": Fore.MAGENTA,
        "RED": Fore.RED,
        "GREEN": Fore.GREEN,
        "YELLOW": Fore.YELLOW,
        "WHITE": Fore.WHITE
    }
    if color.upper() not in colors:
        color = "WHITE"
    print(colors[color.upper()] + message + Fore.RESET)