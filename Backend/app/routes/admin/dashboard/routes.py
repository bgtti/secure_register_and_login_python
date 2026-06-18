# Python/Flask libraries
from flask import Blueprint, request, jsonify
import logging

# Extensions and configurations
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_required

from app.models.user import User
from app.models.stats import UserStats

# Common
# from app.utils.log_event_utils.log import log_event
from app.common.custom_decorators.admin_protected_route import admin_only
from app.common.custom_decorators.json_schema_validator import validate_schema

# Services
from app.services.user.user_flag_service import svc_user_flag_change
from app.services.user.user_service import svc_get_user_by_id, svc_delete_user
from app.services.user.user_role_service import (
    svc_make_user_admin,
    svc_make_user_role_user
)
from app.services.user.user_access_service import svc_set_user_blocked


# JSON Schema


# Blueprint
from . import admin_dash

# In this file: routes concerning admin  

# ----- ADMIN DASHBOARD -----
@admin_dash.route("/admin_dash", methods=["POST"])
@login_required
@admin_only
def admin_dashboard():
    # Daily Active Users (DAU)
    today = datetime.now(timezone.utc).date()

    dau = (
        User.query
        .filter(
            func.date(User.last_seen) == today
        )
        .count()
    )

    #Monthly Active Users (MAU)
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)

    mau = (
        User.query
        .filter(User.last_seen >= thirty_days_ago)
        .count()
    )

    # DAU/MAU Ratio ("stickiness")
    stickiness = dau / mau
    # 5%   -> poor engagement
    # 15%  -> decent
    # 25%+ -> very good
    # 40%+ -> exceptional


    # Churn rate
    # user.created_at
    # user.deleted_at

    # ...
    return jsonify({'response': '...'})