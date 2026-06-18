# Python/Flask libraries
import re

def anonymize_email(email: str) -> str | None:
    """
    Returns anonymous version of email address.

    :param email (str): The email to be anonymized.
    :return (str): The anonymized version of the email.

    Example usage:
    ```python
        print(anonymize_email("john_smith5@fakemail.com"))  # Should return "j***_******@f********.com"
    ```

    """
    if not isinstance(email, str):
        raise ValueError("The provided email must be a string.")
    
    if '@' not in email:
        raise ValueError("The provided email does not contain '@'.")
    
    # function to anonymize string
    def replace_characters(string):
        """
        Example usage:
        ```python
            print(replace_characters("example@domain.com"))  # Output: "*******@******.***"
            print(replace_characters("çüéáö123.456!"))      # Output: "***.***!"
            print(replace_characters(""))                   # Output: ""
            print(replace_characters("a+b-c_d=1"))          # Output: "*+*-*_*=*"
        ```
        """
        if not string or string == "":
            return ""
        # Replace alphabetic characters (including accented ones) and numbers with '*'
        new_string = re.sub(r'[a-zA-Z0-9À-ÖØ-öø-ÿ]', '*', string)
        return new_string

    # Split the string at the last @ available:
    try:
        local_part, domain_part = email.rsplit("@", 1)
    except ValueError:
        raise ValueError("Invalid email format: missing '@'.")
    
    # Deal with the local part: first char remains, and remainder is replaced by * if its a letter or number
    local_first_char = local_part[0]
    local_remainder = local_part[1:] if len(local_part) > 1 else ""
    anonymized_local = f"{local_first_char}{replace_characters(local_remainder)}" 
    
    # Deal with the domain part: split the domain part into server and domain:
    mail_server, *domain_parts = domain_part.rsplit('.', 1)
    domain = f".{domain_parts[0]}" if domain_parts else ""

    mail_server_first_char = mail_server[0]
    mail_server_remainder = mail_server[1:] if len(mail_server) > 1 else ""
    anonymized_domain = f"{mail_server_first_char}{replace_characters(mail_server_remainder)}{domain}" 

    return f"{anonymized_local}@{anonymized_domain}"