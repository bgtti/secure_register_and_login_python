"""
`validation_input_length.py` contains the INPUT_LENGTH dictionary, which define min and max values per variable to be used in JSON schemas for validation of inputs in requests.
"""

INPUT_LENGTH = {
    "name": {
        "minValue": 1,
        "maxValue": 200
    },
    "email": {
        "minValue": 6,
        "maxValue": 320
    },
    # MPTE: Choice of password length: bcrypt has a maximum length input of 72-bytes. Pepper (4chars) and Salt (8chars) are added to password before hashing. If 72 bytes is aprox the same amount in characters, 72 - 4 - 8 = 60.
    "password": { 
        "minValue": 8, #if this value is changed, otp must be changed
        "maxValue": 60
    },
    "otp": {
        "minValue": 8,
        "maxValue": 8
    },
    "contact_message":{
        "minValue": 1,
        "maxValue": 300
    },
    "contact_message_subject":{
        "minValue": 1,
        "maxValue": 45
    },
    "contact_message_answer_subject":{
        "minValue": 1,
        "maxValue": 50
    },
    "honeypot":{
        "minValue": 0,
        "maxValue": 15
    },
    "signed_token":{
        "minValue": 40, # consider 100. Test first though.
        "maxValue": 300, # consider 200. Test first though.
    },
    "encrypted_email":{
        "minValue": 10, # consider 100. Test first though.
        "maxValue": 390, 
    },
    "user_agent": {
        "minValue": 0, 
        "maxValue": 255 
    },
    "form_name":{ # name of front end form (eg: public contact form, login form, etc)
        "minValue": 0, 
        "maxValue": 25 
    },
    "thread_category":{ 
        "minValue": 0, 
        "maxValue": 50 
    },
    "thread_note":{ 
        "minValue": 0, 
        "maxValue": 1000 
    }
}
"""`INPUT_LENGTH` is a dictionary containing the minimum and maximum input length for a number of variables that can be received in json or stored in the database.

The keys: "name", "email", "password", "otp", "contact_message", "contact_message_subject", "contact_message_answer_subject", "honeypot", "signed_token", "encrypted_email", "user_agent"
"""