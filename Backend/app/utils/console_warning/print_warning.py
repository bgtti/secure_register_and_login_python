from colorama import Fore

def console_warn(message, color="BLUE"):
    """
    console_warn(message: str, color: str = "BLUE") -> None
    ------------------------------------------------------------
    Takes a message and displays it in the console.
    Meant to be colored and serve as a warning.

    Optional argument: the color as used in colorama.

    Returns:
        The argument printed to the console in the chosen color.
    ------------------------------------------------------------
    Example usage:

    console_warn("hello", "GREEN") -> prints message in green
    console_warn("hello console") -> prints message in blue once
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