from flask import jsonify

# Blueprint
from . import admin_dash

# In this file: routes concerning admin  

# ----- ADMIN DASHBOARD -----
@admin_dash.route("/admin_dash", methods=["POST"])
def admin_dashboard():
    # ...
    return jsonify({'response': '...'})