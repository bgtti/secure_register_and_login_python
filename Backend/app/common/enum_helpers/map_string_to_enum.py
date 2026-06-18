import logging
from enum import Enum
from typing import Type
from utils.print_to_terminal import print_to_terminal

def map_string_to_enum(value: str | Enum, enum_class: Type[Enum]) -> Enum | None:
    """
    Maps a string value to an Enum member.

    The function performs a case-insensitive lookup by converting
    the provided value to uppercase and matching it against
    the enum member names.

    :param value (str|Enum): String or enum value to map to an enum member.
    :param enum_class (Type[Enum]): Enum class used for lookup.
    
    Example usage:

    ```python
    from app.constants.flags import Flag
    flag = map_string_to_enum("red", Flag)
    # flag => Flag.RED
    ```

    Returns:
        Enum | None: The Enum value or none in case not found.

    """
    try:
        return enum_class[value.upper()]
    except KeyError:
        logging.error(f"User table could not be retrieved as criteria was not met.")
        print_to_terminal(f"Value Error (map_string_to_enum). No such value in {enum_class.__name__}: {value}", "RED")
        return None