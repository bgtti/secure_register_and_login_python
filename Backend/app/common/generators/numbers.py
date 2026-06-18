"""
Docstring for Backend.app.utils.generators.numbers

Keep generators like:
- random numbers
- token generators
"""
# Python/Flask libraries
import secrets

def get_eight_digits_number() -> int: 
    """
    Generates a random 8-digit number.

    The function uses `secrets.randbelow` to generate a secure random number between
    10,000,000 (inclusive) and 99,999,999 (inclusive). This ensures the number is
    always exactly 8 digits long.

    Returns:
        int: A secure random 8-digit number.
    
    More info:
        https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/11-Testing_Multi-Factor_Authentication
    """
    return secrets.randbelow(90000000) + 10000000  # Ensures a 8-digit number
