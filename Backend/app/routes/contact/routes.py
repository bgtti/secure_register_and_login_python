from flask import Blueprint, request, jsonify
import logging
import jsonschema
from flask_login import current_user
from app.extensions import db, limiter
from app.routes.contact.schemas import contact_form_schema
from app.routes.contact.helpers import contact_form_email_forwarding
from app.models.message import Message
from app.models.user import User
from app.utils.custom_decorators.json_schema_validator import validate_schema
from app.utils.log_event_utils.log import log_event
from app.utils.detect_html.detect_html import check_for_html
from app.utils.profanity_check.profanity_check import has_profanity
from app.utils.bot_detection.bot_detection import bot_caught

contact = Blueprint("contact", __name__)

# CONTACT FORM MESSAGES
@contact.route("/contact_form", methods=["POST"])
@limiter.limit("10/day")
@validate_schema(contact_form_schema)
def contactForm():
    """
    contactForm() -> JsonType
    ----------------------------------------------------------
    Route with no parameters.
    Saves a message received through the site's contact form to the db.
    If an email was configured, the message will be forwarded to it.
    Returns Json object containing "response" as string.  
    ----------------------------------------------------------
    Response example:
    response_data = {
            "response":"success"
        } 
    """
    # Standard error response
    error_response = {"response": "There was an error submitting form."}

    # Get the JSON data from the request body
    json_data = request.get_json()
    name = json_data["name"]
    email = json_data["email"]
    message = json_data["message"]
    is_user = json_data["is_user"]
    honeypot = json_data["honeypot"]

    if len(honeypot) > 0:
        bot_caught(request, "signup")
        return jsonify(error_response), 418
    
    # Check if user is a registered user
    # Note the user does not have to be logged in to send a message through the contact form. For this reason, we check whether the user exists both through the cookie and email provided
    # Surely the front end is sending a boolean to indicate whether the user is logged in, and as such, if the user is not logged in on the front end or the backend, we are not checking for the user at all. This was done to save resources, but should you like to be thorough, you may change this logic.
    # PS: it is indeed unlikely that the user is logged in on the FE but does not have the auth cookie...
    is_authenticated = current_user.is_authenticated
    if is_authenticated:
        the_user = User.query.filter_by(email=current_user.email).first()
        is_user = True

    if is_authenticated == False and is_user == True:
        the_user = User.query.filter_by(email=email).first()
        if the_user is None:
            is_user = False

    flag = False

    html_in_name = check_for_html(name, "contact_form - name field", email)
    html_in_email = check_for_html(email, "contact_form - email field", email)
    html_in_message = check_for_html(message, "contact_form - message field", email)

    if html_in_email or html_in_name or html_in_message:
        flag = "YELLOW"
        if is_user:
            log_event("CONTACT_FORM_MESSAGE", "html detected", the_user.id)
            the_user.flag_change(flag)
        else:
            log_event("CONTACT_FORM_MESSAGE", "html detected")
    else:
        profanity_in_name = has_profanity(name) 
        profanity_in_email = has_profanity(email)
        profanity_in_message = has_profanity(message)
        if profanity_in_name or profanity_in_email or profanity_in_message:
            flag = "PURPLE"
            if is_user:
                log_event("CONTACT_FORM_MESSAGE", "profanity", the_user.id)
                the_user.flag_change(flag)
            else:
                log_event("CONTACT_FORM_MESSAGE", "profanity")

    # Create message
    try:
        new_message = Message(sender_name=name, sender_email=email, message=message) 
        db.session.add(new_message)
        if flag:
            new_message.flag_change(flag)
        if is_user:
            new_message.user_id = the_user.id
        db.session.commit()

    except Exception as e:
        logging.error(f"Failed to save message. Error: {e}")
        try:
            log_event("CONTACT_FORM_MESSAGE", "message failed")
        except Exception as e:
            logging.error(f"Log event error for failed message. Error: {e}")
        return jsonify(error_response), 500

    # Log event to user and system logs
    try:
        logging.info(f"New message received.")
        log_event("CONTACT_FORM_MESSAGE", "message successful")
    except Exception as e:
        logging.error(f"Log event error for sucessful message. Error: {e}")

    # Forward contact form message per email
    # In the case the form provided email is different than the one in the db, sending the registered email...
    email_in_db = ""
    if is_user:
        email_in_db = the_user.email
    try:
        email_forwarded = contact_form_email_forwarding(name, email, message, is_user, email_in_db)
    except Exception as e:
        logging.error(f"Email forwarding issue. Error: {e}")

    if not email_forwarded:
        logging.error(f"An error prevented the contact form message to be forwarded to the email address provided. Please check the config file.")

    response_data ={
            "response":"success"
        }
    return jsonify(response_data)