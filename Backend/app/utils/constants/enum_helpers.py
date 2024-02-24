import logging

def map_string_to_enum(value, enum_class):
    """
    map_string_to_enum(value: str, enum_class: class) -> enum
    ------------------------------------------------------------
    Parameters: the string value which can be traced to an enum class and the enum class
    Returns: the enum
    ------------------------------------------------------------
    Example usage:
    
    from app.utils.constants.enum_class import UserFlag
    map_string_to_enum("red", UserFlag) -> UserFlag.RED
    """
    try:
        return enum_class[value.upper()]
    except KeyError:
        logging.error(f"User table could not be retrieved as criteria was not met.")
        raise ValueError(f"No such value in {enum_class.__name__}: {value}")