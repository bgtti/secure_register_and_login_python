"""
In this file: routes that receives and saved messages from the contact form.

Note: only basic logging implemented here. More robust logging logic may be necessary.
"""

# Python/Flask libraries
from flask import Blueprint, request, jsonify
import logging

# Extensions and configurations
import jsonschema
from flask_login import current_user
from app.extensions.extensions import db, limiter

# Constants 
from app.constants.message_and_thread import MessageDirection, MessageChannel

# Utilities
from app.common.custom_decorators.json_schema_validator import validate_schema
from app.common.ip_utils.ip_address_validation import get_client_ip
from app.common.ip_utils.ip_geolocation import geolocate_ip
from app.common.ip_utils.ip_anonymization import anonymize_ip

# Services
from app.services.user.user_service import svc_get_user_or_none
from app.services.message.add_thread_service import svc_start_message_thread

# Email services
from app.emails.contact.contact_form_forwarding_email import forward_contact_form_to_apps_email

# Json Schemas
from app.routes.contact.schemas import contact_form_schema

contact = Blueprint("contact", __name__)

# CONTACT FORM MESSAGES
@contact.route("/contact_form", methods=["POST"])
@limiter.limit("10/day")
@validate_schema(contact_form_schema)
def contact_form():  
    """
    Saves a message received through the site's contact form to the DB.
    If an email was configured in the app, the message will be forwarded to it.

    If messaged is saved, will return a successful response even if email forwarding fails.
    
    Possible responses: 200, 500.
    """
    # Get the JSON data from the request body
    json_data = request.get_json()
    name = json_data["name"]
    email = json_data["email"]
    subject = json_data.get("subject", "no subject")
    message = json_data["message"]
    user_agent = json_data.get("user_agent", "")
    honeypot = json_data["honeypot"] # TODO: rename

    # Get the request ip
    client_ip = get_client_ip(request) or ""

    # responses
    error_response = {"response": "There was an error submitting form."}
    success_response ={"response":"success"}

    # Ignore obvious bots
    if len(honeypot) > 0:
        # bot_caught(request, "signup")
        logging.info(f"Bot caught in honeypot. Route: contact_form. IP: {client_ip}")
        return jsonify(success_response), 200
    
    # geo
    geo_ip = geolocate_ip(client_ip)
    ip_location = f"Country: {geo_ip['country']}, city: {geo_ip['city']}, proxy: {geo_ip['proxy']}, hosting: {geo_ip['hosting']}"
    
    # Note the user does not have to be logged in to send a message through the contact form. For this reason, we check whether the user exists both through the cookie and email provided. If user is logged in but enters a different email address in the contact form field, we make a note of this.
    is_authenticated = bool(current_user and current_user.is_authenticated)
    user = svc_get_user_or_none(email, "contact_form")

    note = None
    if is_authenticated and current_user.email != email:
        if user and user.id:
            note = f"Authenticated user submitted contact form using an email that belongs to another user. Authenticated email: {current_user.email}. Submitted email: {email}."
        else:
            note = f"Authenticated user email differed from submitted contact email. Authenticated email: {current_user.email}. Submitted email: {email}."

    if is_authenticated:
        originator_user_id = current_user.id
    else:
        originator_user_id = user.id if user else 0

    thread_res = svc_start_message_thread(
        originator_user_id = originator_user_id, 
        originator_email = email, 
        originator_name = name, 
        subject = subject, 
        message_body = message,
        direction = MessageDirection.INBOUND,
        channel = MessageChannel.CONTACT_FORM,
        user_agent = user_agent,
        ip_address = anonymize_ip(client_ip),
        geo_location = ip_location,
        recipient_id=0, # system
        recipient_email="app@support", #NOTE: change default
        recipient_name="Support",
        note_about_thread = note,
        )
    
    if not thread_res["success"]:
        logging.error(f"Contact form failed. {thread_res.get('log_txt')}")
        return jsonify(error_response), 500
    
    logging.info("New message received via contact form. Thread and message created.")

    # Forward contact form message per email
    email_ok = forward_contact_form_to_apps_email(name, email, subject, message, note)
    
    if not email_ok:
        logging.error(f"Contact form could not be forwarded to app's email.")

    return jsonify(success_response), 200