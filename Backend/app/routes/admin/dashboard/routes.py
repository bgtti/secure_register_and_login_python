from flask import Blueprint, jsonify

admin_dash = Blueprint('admin_dash', __name__)

# In this file: routes concerning admin  

# ----- ADMIN DASHBOARD -----
@admin_dash.route("/admin_dash", methods=["POST"])
def admin_dashboard():
    # ...
    return jsonify({'response': '...'})