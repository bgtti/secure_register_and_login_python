# Python and Flask
from datetime import datetime, timezone, timedelta
import logging

# DB Models
from app.models.user import User
from app.models.role import Role

# Constants
from app.constants.flags import Flag

# Common Utils
from app.common.enum_helpers.map_string_to_enum import map_string_to_enum

def svc_get_users_table(
    page_nr: int,
    items_per_page: int = 25,
    order_by: str = "last_seen", #["last_seen", "name", "email", "created_at"]
    order_sort: str = "descending", #["descending", "ascending"]
    filter_by: str = "none", #["none", "is_blocked", "is_unblocked", "flag", "flag_not_blue","is_admin", "is_user", "last_seen"]
    filter_by_flag: str = "blue",
    filter_by_last_seen: str = "",
    search_by: str = "none", #["none", "name", "email"]
    search_word: str = "",
) -> dict | None:
    """
    Retrieves a paginated list of users for the admin users table.
    Super admins are excluded from the result.

    :param page_nr (int): the page number, must be greater than 0.
    :param items_per_page (int): number of user items, must be greater than 0. Defaults to 25.
    :param order_by (str): one of: ["last_seen", "name", "email", "created_at"]. Defaults to "last_seen".
    :param order_sort (str) one of: ["descending", "ascending"]. Defaults to "descending".
    :param filter_by (str): one of: ["none", "is_blocked", "is_unblocked", "flag", "flag_not_blue","is_admin", "is_user", "last_seen"]. Defaults to "none".
    :param filter_by_flag (str): must be member of enum Flag. Defaults to "blue".
    :param filter_by_last_seen (str): date formatted yyyy-mm-dd (eg: 2026-05-24). Defaults to "".
    :param search_by (str): one of: ["none", "name", "email"]. Defaults to "none".
    :param search_word (str): free string. Defaults to "".

    Returns:
        dict | None: None if no users are found, otherwise a dictionary containing: current_page (int), total_pages (int), and users (list of user dict)
    
    Example of return data:
    ```python
    {
        "current_page": 1,
        "total_pages": 5,
        "users": [
            {
            "id": 10
            "name": "Frank Torres",
            "email": "frank.torres@fakemail.com",
            "last_seen": "Thu, 25 Jan 2024 00:00:00 GMT",
            "access": "user",
            "flagged": "blue",
            "is_blocked": "false"
            }, 
            #...
        ]
    }
    ```
    """
    # Check params
    if page_nr < 1 or items_per_page < 1:
        logging.error("svc_get_users_table received wrong int params.")
        return None
    
    # Filter out super_admin
    query = User.query.join(Role).filter(
        Role.access_level != "super_admin"
    )

    # Allow ordering by one of ["last_seen", "name", "email", "created_at"]
    ordering = {
        "last_seen": User.last_seen,
        "name": User.name,
        "email": User.email,
        "created_at": User.created_at,
    }.get(order_by)

    if ordering is None:
        return None

    # Sort table 
    if order_sort == "descending":
        ordering = ordering.desc()
    else:
        ordering = ordering.asc()

    # Convert "yyyy-mm-dd" into timezone-aware datetime or default to now - 30 days (users active in the last 30 days)
    if filter_by_last_seen:
        filter_by_last_seen = datetime.strptime(
            filter_by_last_seen,
            "%Y-%m-%d"
        ).replace(tzinfo=timezone.utc)
    else:
        filter_by_last_seen = datetime.now(timezone.utc) - timedelta(days=30)

    # Filter table options: ["none", "is_blocked", "is_unblocked", "flag", "flag_not_blue","is_admin", "is_user", "last_seen"]
    if filter_by != "none":
        filter_conditions_map = {
            "is_blocked": User.is_blocked.is_(True),
            "is_unblocked": User.is_blocked.is_(False),
            "flag": User.flagged == map_string_to_enum(filter_by_flag, Flag),
            "flag_not_blue": User.flagged != Flag.BLUE,
            "is_admin": Role.access_level == "admin",
            "is_user": Role.access_level == "user",
            "last_seen": User.last_seen >= filter_by_last_seen,
        }

        filter_condition = filter_conditions_map.get(filter_by)

        if filter_condition is None:
            logging.error("svc_get_users_table invalid filter_by.")
            return None

        query = query.filter(filter_condition)

    # Search table by one of: ["none", "name", "email"]
    if search_by != "none" and search_word:
        search_word = search_word.strip()
        search_conditions_map = {
            "name": User.name.ilike(f"%{search_word}%"),
            "email": User.email.ilike(f"%{search_word}%"),
        }

        search_condition = search_conditions_map.get(search_by)

        if search_condition is None:
            logging.error("svc_get_users_table invalid search_by.")
            return None

        query = query.filter(search_condition)

    users = query.order_by(ordering).paginate(
        page=page_nr,
        per_page=items_per_page,
        error_out=False
    )

    if not users.items:
        return None

    def serialize(user):
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at,
            "last_seen": user.last_seen,
            "access": user.role.access_level,
            "flagged": user.flagged.value,
            "is_blocked": user.is_blocked,
        }

    return {
        "users": [serialize(user) for user in users.items],
        "total_pages": users.pages,
        "current_page": users.page,
    }