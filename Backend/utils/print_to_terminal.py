"""
**ABOUT THIS FILE**

print_to_terminal.py contains the function **print_to_terminal** which prints messages to the terminal in different colours. Can be helpful to warn of errors during development.

"""
from colorama import Fore

def print_to_terminal(message: str, color: str = "BLUE") -> None:
    """
    Prints a message to the terminal in a specified color.

    This function takes a message and an optional color parameter to print the message
    to the terminal in the given color. It is designed to enhance terminal output visibility
    and is often used for warnings or important information.

    ------------------------------------------------------------

    **Parameters:**
        message (str): The message to be printed to the terminal.
        color (str, optional): The color in which the message will be printed (as used in colorama).

    **Colour options:**
        "BLUE", "CYAN", "MAGENTA", "RED", "GREEN", "YELLOW", "WHITE".

    **Returns:**
        None: The message printed to the terminal in the chosen colour.

    ------------------------------------------------------------
    **Example usage:**

        ```python
        print_to_terminal("hello", "GREEN") # -> prints message in green
        print_to_terminal("hello console") # -> prints message in blue once
        ```
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