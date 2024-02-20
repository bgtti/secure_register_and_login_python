import logging
from app.extensions import db
from app.models.bot_catch import BotCatch
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.ip_utils.ip_geolocation import geolocate_ip 

def bot_caught(request, form_targeted):
    """
    bot_caught(request: obj, form_targeted: str) -> void
    ------------------------------------------------------------
    Parameters: the request object and form whose honeypot the bot was caught in.
    Function adds the bot to the db and logs the information.
    ------------------------------------------------------------
    Example usage:
    
    if honeypot != "":
        bot_caught(request, "login")
        return jsonify(error_response), 418
    """
    client_ip = get_client_ip(request)

    if client_ip:
        geolocation = geolocate_ip(client_ip)
        country = geolocation["country"]
    else:
        client_ip = "unkown" 
        country = "unkown" 

    json_data = request.get_json()
    user_agent = json_data["user_agent"]

    try:
        new_bot = BotCatch(client_ip, country, user_agent, form_targeted)
        db.session.add(new_bot)
        db.session.commit()
        logging.info(f"Bot caught submitting form: {form_targeted}")
    except Exception as e:
        logging.error(f"Could not add caught bot to the database. Error: {e}")
    
    return

