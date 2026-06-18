"""
"""
import logging
from urllib.parse import urlparse
from app.extensions.extensions import db
from app.models.bot_trap import BotTrap
from app.common.ip_utils.ip_address_validation import get_client_ip
from app.common.ip_utils.ip_geolocation import geolocate_ip 

def svc_bot_caught(request: object, form_targeted: str, endpoint: str) -> None: 
    """
    Function in `services/bot/bot_service.py`.
    Adds and commits bot info to the db tale BotTrap. Use if honeypot trigerred.
    This service will not raise errors.
    *PS: this function does not create a security log.*

    --------
    **Fields overview**:

    :param request: request headers
    :param form_targeted: string with name of the form (in FE)
    :param endpoint: string with name of the endpoint that received honeypot value

    --------
    **Example usage**:
    ```
    from flask import request
    if honeypot != "":
        svc_bot_caught(request, "login", "/api/login")
        return jsonify({"status": "verification_required"}), 202 
    ```  
    """
    if not isinstance(form_targeted, str) or not isinstance(endpoint, str):
        logging.error(f"Bot information could not be added to the DB due to malformed call to svc_bot_caught.")
        return None
    
    # IP and Geolocation
    ip_address = get_client_ip(request)

    if ip_address:
        try:
            location = geolocate_ip(ip_address) or {}
            geo_location = f"{location.get('city','N/A')}, {location.get('country','N/A')}"
        except Exception:
            logging.error("geolocate_ip failed when called by svc_bot_caught")
    else:
        ip_address = "unknown" 
        geo_location = "unknown" 

    # User agent
    user_agent = request.headers.get("User-Agent")
    # if user agent not in header, try getting it from json
    if not user_agent:
        json_data = request.get_json(silent=True) or {}
        user_agent = json_data.get("user_agent")
    if isinstance(user_agent, str) and len(user_agent) > 250:
        user_agent = user_agent[:250]
    
    # Referrer origin
    referrer = None
    ref = request.referrer
    if isinstance(ref, str) and ref:
        parsed = urlparse(ref)
        if parsed.scheme and parsed.netloc:
            referrer = f"{parsed.scheme}://{parsed.netloc}"

    try:
        new_bot = BotTrap(
            form_targeted=form_targeted,
            endpoint=endpoint,
            ip_address=ip_address, 
            geo_location=geo_location, 
            user_agent=user_agent,
            referrer=referrer, 
            )
        db.session.add(new_bot)
        db.session.commit()
        logging.info(f"Bot caught submitting form: {form_targeted}")
    except Exception as e:
        db.session.rollback()
        logging.error(f"BotTrap insert failed. Error: {e}")
    
    return None

"""
The above are for bots caught in honeypot

recommended for 'suspected bots':

def detect_bot(request):
    ua = request.headers.get("User-Agent", "")
    ip = request.remote_addr
    
    # Suspicious user-agent
    if ua.lower().startswith(("python", "curl", "wget", "go-http", "java")):
        log_security_event(SecurityEvent.BOT_SUSPECTED, details={"ua": ua})

    # Very fast form submission
    if time_since_page_load(request) < 0.1:
        log_security_event(SecurityEvent.BOT_SUSPECTED, details={"speed": "too_fast"})

    # Repeated invalid CSRF
    if request_has_repeated_invalid_csrf(request):
        log_security_event(SecurityEvent.BOT_SUSPECTED, details={"reason": "csrf"})
    
    # Known bot IP ranges
    if ip_in_cloud_provider_range(ip):
        log_security_event(SecurityEvent.BOT_SUSPECTED, details={"ip": ip})

    # Constant request intervals
    if is_robotic_request_pattern(user=request.user):
        log_security_event(SecurityEvent.BOT_SUSPECTED, details={"pattern": "robotic"})

"""