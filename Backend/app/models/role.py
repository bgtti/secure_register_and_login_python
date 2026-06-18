"""
**ABOUT THIS FILE**

models/role.py contains:

- Constants required for the db model or methods to function
- Helper functions used only in the db model or methods 
- **Role** class (the db model)

**Access is defined by role ID.**
Each role has specific permissions in the app.
A user can be assigned one role only.
"""
# Python/Flask libraries
from datetime import datetime, timezone

# Extensions and configurations
from flask_login import UserMixin
from sqlalchemy import event
from app.extensions.extensions import db
from app.extensions.sqlalchemy_config import UTCDateTime

# Constants
from constants.roles import ROLES


# TODO: implement in user model. Currently not implemented or used anywhere

"""
Module           | Task                                             | Access role               
None               Use the site/ user dashboard                       User
User               View user account details                          Customer support, admin, super
User               Change user role                                   Super
User               Delete user, Reset MFA, Email change, block user   admin, super
Messages           View messages, respond to messages, flag content   Customer support, admin, super
Messages           Delete messages                                    admin, super
Logs               View logs                                          Customer support, admin, super
Logs               Change log level, delete log                       admin, super
Support            Ticket                                             Customer support, admin, super
Newsletters        View, create, edit, send                           content writer, admin, super
Newsletters        Approve sending                                    admin, super
Stats              View                                               admin, super
Role               View, creation                                     super
Permission         View, creation                                     super

"""

"""
Permission versus Role-basedaccess control

The choice here was simplicity: instead of managing a great number of permission, the decision was made to manage access role-based instead.
Should this software be used for a small team, this should make sense.
One should migrate to permission-based when scaling up or in case the app team needs highly customized permissions.
"""



class Role(db.Model, UserMixin):
    """
    Role db model's purpose is to define role-based access.

    --------------------------------------------------------------
    Fields overview:

    - name of role: As defined in ROLES array. Examples: User, Admin, Super Admin
    - access_level: As defined in ROLES array. Example: user, admin, super_admin
    - default:      Boolean value. Only true for role "User" and false for all others. 
    
    """
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    created_at = db.Column(UTCDateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    name = db.Column(db.String(64), unique=True)
    access_level = db.Column(db.String(20), unique=True)
    default = db.Column(db.Boolean, default=False, nullable=False, index=True) # should be set to True only for one role and False for all others. The role marked as default will be assigned to new users upon registration.
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        
    @staticmethod
    def insert_roles():
        """ 
        Inserts roles into the database if they do not exist. 
        This method is called during the app initialization (scripts/setup.py).
        """
        default_role_name = "User"  # Set "User" as the default role

        for role_data in ROLES:
            role = Role.query.filter_by(name=role_data["name"]).first()
            if not role:
                role = Role(
                    id=role_data["id"],  # Setting fixed ID
                    name=role_data["name"],
                    access_level=role_data["access_level"],
                    default=(role_data["name"] == default_role_name)  # Only "User" should be default
                )
                db.session.add(role)
        
        db.session.commit()  

# TODO WARNING: the bellow may not work ---- during creation, target.id is not None.
@event.listens_for(Role.default, "set", retval=True)
def prevent_default_change(target, value, oldvalue, initiator):
    """
    Prevent changing `default` after the row already exists.
    Allows setting it during initial creation.
    """
    # When the object is already in DB and value is changing
    if target.id is not None and oldvalue is not None and value != oldvalue:
        raise ValueError("The `default` flag on Role is read-only once set.")
    return value