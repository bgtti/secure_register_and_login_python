from flask import Blueprint, request, jsonify
from datetime import datetime, timezone, timedelta
from flask_login import login_required, current_user
from app.extensions import limiter, db
from sqlalchemy.exc import IntegrityError
import logging
from app.models.user import User
from app.models.log_event import LogEvent
from app.models.message import Message
from app.utils.constants.enum_class import modelBool, UserAccessLevel, UserFlag
from app.utils.constants.enum_helpers import map_string_to_enum
from app.utils.detect_html.detect_html import check_for_html
from app.utils.custom_decorators.admin_protected_route import admin_only
from app.utils.custom_decorators.json_schema_validator import validate_schema
from app.routes.admin.message_action.schemas import admin_message_action_mark_as, admin_message_action_flag_change, admin_message_action_mark_answer, admin_message_delete_schema
from app.routes.admin.message_action.helpers import set_spammer


message_action = Blueprint('message_action', __name__)

# In this file: routes that provide message-related information (to be accessed by admin users only) 
#   - table with all messages, 
#   - message actions

# View functions in this file provide and/or modify information in the db


# ----- MESSAGES MARK AS ----- #---------------------># TODO: block user that is marked as spammer
@message_action.route("/mark_as", methods=["POST"])
@login_required
@admin_only
@validate_schema(admin_message_action_mark_as)
def mark_as():
    """
    mark_as() -> JsonType
    ----------------------------------------------------------
    Route to mark a message as spam or answer needed.
    Takes a JSON payload with the following required parameters:
    - "message_id": the id of the message to be marked (int)
    - "answer_needed": boolean indicating whether answer is needed.
    - "is_spam": boolean indicating whether message is spam.
    - "sender_is_spammer": boolean indicating whether sender should be included in the spammer list.

    Note that if message is marked as spam, it will automatically be marked as no answer needed.
    
    Returns a JSON object with a "response" field.
    ----------------------------------------------------------
    Request example:
    json_payload = {
        "message_id": 6,
        "answer_needed": true,
        "is_spam": false
        "sender_is_spammer": false
    }
    ----------------------------------------------------------
    Response examples:

    {"response": "Requested page out of range"}

    {"response":"success",
    "requested":{
        "message_id": 6,
        "answer_needed": true,
        "is_spam": false,
        "sender_is_spammer": false
    }
    }
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get info from JSON payload
    message_id = json_data["message_id"] 
    answer_needed = json_data["answer_needed"] 
    is_spam = json_data["is_spam"] 
    sender_is_spammer = json_data["sender_is_spammer"]

    try:
        the_message = Message.query.filter_by(id=message_id).first()

        if not the_message:
            logging.warning(f"Message id={message_id} could not be found, 404 not found.") 
            return jsonify({"response": "Message not found"}), 404
        
        if is_spam is True:
            the_message.mark_spam()
            if sender_is_spammer is True:
                admin_id = current_user.id
                spammer_added = set_spammer(admin_id, the_message.sender_email)
                if not spammer_added:
                    logging.error(f"Setting Spammer failed: returning error 500 from mark_message_as api.")
                    return jsonify({"response": "Failed to mark sender as spammer"}), 500
        else:
            if the_message.is_spam == modelBool.TRUE:
                the_message.is_spam = modelBool.FALSE
                the_message.flagged = UserFlag.BLUE
            if answer_needed is True:
                the_message.reply_needed()
            if answer_needed is False:
                the_message.no_reply_needed()
        
        db.session.commit()
        logging.info(f"Message id={message_id} has been marked succesfully.") 
        
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"DB integrity error prevented message to be marked: {e}")
        return jsonify({"response": "Integrity error prevented message to be marked."}), 500
    
    except Exception as e:
        logging.error(f"Error prevented message to be marked: {e}")
        return jsonify({"response": "Error prevented message to be marked."}), 500

    response_data ={
            "response":"success",
            "requested":{
                "message_id": message_id,
                "answer_needed": answer_needed,
                "is_spam": is_spam,
                "sender_is_spammer":sender_is_spammer
            }
        }
    
    return jsonify(response_data)


# ----- MESSAGES FLAG CHANGE -----
@message_action.route("/flag_change", methods=["POST"])
@login_required
@admin_only
@validate_schema(admin_message_action_flag_change)
def flag_change():
    """
    flag_change() -> JsonType
    ----------------------------------------------------------
    Route to change a message's flag.
    Takes a JSON payload with the following required parameters:
    - "message_id": the id of the message to be edited (int)
    - "message_flag": the new flag colour that must be value from UserFlag enum class (str)
    
    Returns a JSON object with a "response" field.
    ----------------------------------------------------------
    Request example:
    json_payload = {
        "message_id": 6,
        "message_flag": "blue"
    }
    ----------------------------------------------------------
    Response examples:

    {"response":"success",
    "requested":{
        "message_id": 6,
        "answer_needed": true,
        "is_spam": false,
        "sender_is_spammer": false
    }
    }

    {"response": "Message not found"}
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get info from JSON payload
    message_id = json_data["message_id"] 
    message_flag = json_data["message_flag"] 

    # Make sure flag exists
    flag = map_string_to_enum(message_flag, UserFlag)
    if flag == None:
        return jsonify({"response": "Flag colour not found"}), 404

    try:
        the_message = Message.query.filter_by(id=message_id).first()

        if not the_message:
            logging.info(f"Message id={message_id} could not be found, 404 not found.") 
            return jsonify({"response": "Message not found"}), 404
        
        the_message.flag_change(message_flag)
        
        db.session.commit()
        
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"DB integrity error prevented message to be flagged: {e}")
        return jsonify({"response": "Integrity error prevented message to be flagged."}), 500
    
    except Exception as e:
        logging.error(f"Error prevented message to be flagged: {e}")
        return jsonify({"response": "Error prevented message to be flagged."}), 500

    response_data ={
            "response":"success",
            "requested":{
                "message_id": message_id,
                "message_flag": message_flag,
            }
        }
    
    return jsonify(response_data)

# ANSWER MESSAGE
@message_action.route("/mark_answer", methods=["POST"])
@login_required
@admin_only
@validate_schema(admin_message_action_mark_answer)
def mark_answer():
    """
    mark_answer() -> JsonType
    ----------------------------------------------------------
    Route to change a message's flag.
    Takes a JSON payload with the following required parameters:
    - "message_id": the id of the message to be edited (int)
    - "answered_by": email of admin who answered (str)
    - "answer": answer text (str)
    - "email_answer": whether message should be sent by email (bool)
    
    Returns a JSON object with a "response" field.
    ----------------------------------------------------------
    Request example:
    json_payload = {
        "message_id": 6,
        "answered_by": "example@fakemail.com",
        "answer": "Hi George, we are working to solve your issue."
        "email_answer": false
    }
    ----------------------------------------------------------
    Response examples:

    {"response":"success",
        "requested":{
            "message_id": 6,
            "answered_by": "example@fakemail.com",
            "answer": "Hi George, we are working to solve your issue."
        }
    }

    {"response": "Message not found"}
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get info from JSON payload
    message_id = json_data["message_id"] 
    answered_by = json_data["answered_by"]
    answer = json_data["answer"]
    email_answer = json_data["email_answer"]
    answer_date = datetime.strptime(json_data["answer_date"], "%Y-%m-%d").date() if "answer_date" in json_data else datetime.now(timezone.utc)
    subject = json_data["subject"] if "subject" in json_data else "Re: contact form submission"

    # Debug log
    logging.debug(f"Request to record answer received: Message id={message_id}, answered_by={answered_by}, answer={answer}, answer_date={answer_date}. answer_date is request: {'Yes' if 'answer_date' in json_data else 'No'} ") 

    # In case answer should be sent per email
    #if email_answer is True:
        #TODO
        # Do not forget: answerBy... is it now the email of the user or the system?
        # -> it must be known who sent it...
        # Import message_action_answer_message from helpers

    # Record the answer in db
    try:
        the_message = Message.query.filter_by(id=message_id).first()

        if not the_message:
            logging.info(f"Message id={message_id} could not be found, 404 not found.") 
            return jsonify({"response": "Message not found"}), 404
        
        the_message.message_answered(answered_by,answer,answer_date)
        
        db.session.commit()
        
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"DB integrity error prevented message id={message_id} answer to be recorded: {e}")
        return jsonify({"response": "Integrity error prevented message answer to be recorded."}), 500
    
    except Exception as e:
        logging.error(f"Error prevented message id={message_id} answer to be recorded: {e}")
        return jsonify({"response": "Error prevented message answer to be recorded."}), 500
    
    # In case answer_by email is different from that of the admin user, log that fact
    try:
        user = current_user
        if user.email != answered_by:
            logging.info(f"Admin with id {user.id} recorded a message answer answered by {answered_by} but own email is {user.email}")
    except Exception as e:
        logging.error(f"Error prevented log of answer to be recorded: {e}")


    response_data ={
            "response":"success",
            "requested":{
                "message_id": message_id,
                "answered_by": answered_by,
                "answer": answer,
                "answer_date": answer_date
            }
        }
    
    return jsonify(response_data)  
    
    

# ----- ACTION: DELETE Message ----- 
@message_action.route("/delete_message", methods=["POST"])
@login_required
@admin_only
@validate_schema(admin_message_delete_schema) 
def delete_message():
    """
    delete_message() -> JsonType
    ----------------------------------------------------------
    Route to delete a message by id.
    Takes a JSON payload with the following parameters:
    - "message_id": Message's id to be deleted.

    Returns a JSON object with a "response" field:
    - If deletion is successful: {"response": "success"}
    - If the id is not found: {"response": "Message not found"}
    - If an error occurs during deletion: {"response": "Error deleting message", "error": "Details of the error"}

    ----------------------------------------------------------
    Request example:
    json_payload = {
        "message_id": 12345
    }
    ----------------------------------------------------------
    Response examples:
    {"response": "success"}
    {"response": "Message not found"}
    {"response": "Error deleting message", "error": "Details of the error"}
    """
    # Get the JSON data from the request body
    json_data = request.get_json()

    # Get id from JSON payload
    message_id = json_data["message_id"]

    try:
        the_message = Message.query.filter_by(id=message_id).first()

        if not the_message:
            logging.info(f"Message id={message_id} could not be found, 404 not found.") 
            return jsonify({"response": "Message not found"}), 404
        
        db.session.delete(the_message)
        
        db.session.commit()
        
        logging.info("Message deleted successfully.")
        #log_event("ADMIN_DELETE_USER","deletion successful",user.id, f"Admin action from: {current_user.email}.")

        return jsonify({"response": "success"})

    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"DB integrity error prevented message deletion: {e}")
        #log_event("ADMIN_DELETE_USER","deletion problem",user.id)
        return jsonify({"response": "Error deleting message"}), 500

    except Exception as e:
        logging.error(f"Error prevented message deletion: {e}")
        #log_event("ADMIN_DELETE_USER","deletion problem",user.id)
        return jsonify({"response": "Error deleting message"}), 500