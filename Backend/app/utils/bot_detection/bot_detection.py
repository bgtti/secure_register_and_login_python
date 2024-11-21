import logging
from app.extensions.extensions import db
from app.models.bot_catch import BotCatch
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.ip_utils.ip_geolocation import geolocate_ip 

def bot_caught(request, form_targeted):
    """
    bot_caught(request: obj, form_targeted: str) -> None
    ------------------------------------------------------------
    Parameters: the request object and form whose honeypot the bot was caught in.
    Function adds the bot to the db and logs the information.
    If the function fails to add bot to the db, it will not return an error (it always returns None).
    ------------------------------------------------------------
    Example usage:
    
    if honeypot != "":
        bot_caught(request, "login")
        return jsonify(error_response), 418
    """
    ip_address = get_client_ip(request)

    if ip_address:
        geolocation = geolocate_ip(ip_address)
        country = geolocation["country"]
    else:
        ip_address = "unknown" 
        country = "unknown" 

    try:
        json_data = request.get_json()
        user_agent = json_data["user_agent"]
        new_bot = BotCatch(ip_address=ip_address, country=country, user_agent=user_agent, form_targeted=form_targeted)
        db.session.add(new_bot)
        db.session.commit()
        logging.info(f"Bot caught submitting form: {form_targeted}")
    except Exception as e:
        logging.error(f"Could not add caught bot to the database. Error: {e}")
    
    return None

