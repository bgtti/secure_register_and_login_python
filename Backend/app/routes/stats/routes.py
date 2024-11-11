from flask import Blueprint, request, jsonify, session
from datetime import datetime
from hashlib import sha256
from uuid import uuid4
import logging
import jsonschema
import requests
from app.extensions.extensions import flask_bcrypt, db, limiter
from app.models.stats import VisitorStats
from app.routes.stats.schemas import analytics_schema
# from app.stats.helpers import anonymize_ip
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.ip_utils.ip_anonymization import  anonymize_ip

stats = Blueprint("stats", __name__)

@stats.route("/analytics", methods=["POST"])
@limiter.limit("1000/day")
def analytics():
    """
    analytics() -> JsonType
    ----------------------------------------------------------
    Route with no parameters.
    Sets a session cookie in response.
    Will always return 200 even if db error occurs.
    ----------------------------------------------------------
    Response always:
    response_data = {
            "response":"success"
        } 
    """
    # Get the JSON data from the request body
    json_data = request.get_json()
    page = json_data["page"]
    referrer = json_data["referrer"]
    screen_size = json_data["screen_size"]
    operating_system = json_data["operating_system"]
    user_agent = json_data["user_agent"]

    # Validate the JSON data against the schema
    try:
        jsonschema.validate(instance=json_data, schema=analytics_schema)
    except jsonschema.exceptions.ValidationError as e:
        logging.error(f"Stats error: Jsonschema validation. Error: {str(e)}")
        page = request.referrer
        referrer = ""
        screen_size = ""
        operating_system = ""
        user_agent = ""

    # Check if there is a visitor session and if so, if geolocation already exists
    visitor_session_id = session.get("visitor_session_id")
    needs_geolocation = visitor_session_id is None
    
    client_ip = get_client_ip(request)

    continent = ""
    country = ""
    country_code = ""
    city = ""

    if needs_geolocation is False:
        try:
            visitor_stats = VisitorStats.query.filter_by(session_visit=visitor_session_id).first()
            if visitor_stats is not None:
                continent = visitor_stats.continent
                country = visitor_stats.country
                country_code = visitor_stats.country_code
                city = visitor_stats.city
            else:
                # on local expect client_ip to be "127.0.0.1"
                if client_ip != "127.0.0.1":
                    needs_geolocation = True
        except Exception as e:
            logging.debug(f"Stats error: Failed to get visitor stats. Visitor session: {visitor_session_id}. Error: {str(e)}")

    if needs_geolocation is True:
        # set session cookie
        visitor_session_id = uuid4().hex
        session["visitor_session_id"] = visitor_session_id
        # get geolocation from ip-api
        query_url = f"http://ip-api.com/json/{client_ip}?fields=status,message,continent,country,countryCode,city"
        
        try:
            ip_info_request = requests.get(query_url)
            ip_info = ip_info_request.json()
        except Exception as e:
            logging.debug(f"Stats error: Failed to get geolocation of IP. Error: {str(e)}")
        if ip_info and ip_info["status"] == "fail":
            logging.debug(f"Stats error: Geolocation query failed. Message: {ip_info["message"]}")
        elif ip_info:
            continent = ip_info["continent"]
            country = ip_info["country"]
            country_code = ip_info["countryCode"]
            city = ip_info["city"]

    # is ip address cant be anonymized, hash it
    anonymized_ip = anonymize_ip(client_ip)
    if anonymized_ip is None:
        anonymized_ip = sha256(client_ip.encode('utf-8')).hexdigest()
    
    try:
        new_page_hit = VisitorStats(
            ip_address=anonymized_ip, 
            continent=continent,
            country=country,
            country_code=country_code,
            city=city,
            user_agent=user_agent,
            os=operating_system,
            screen_size=screen_size,
            referrer=referrer,
            page_accessed=page,
            session_visit = visitor_session_id
            )
        db.session.add(new_page_hit)
        db.session.commit()
        logging.debug(f"New stats added.")

    except Exception as e:
        logging.error(f"Stats error: VisitorStats could not be added. Error: {e}")
    
    return jsonify(success=True)