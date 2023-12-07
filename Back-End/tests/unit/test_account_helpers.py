# import unittest
from app.account.helpers import is_good_password

def test_is_good_password():
    """
    GIVEN a password
    CHECK whether it meets the criteria for a safe password
    """
    # Sequential characters check: Characters should not be repeated 4 or more times in sequence
    assert is_good_password("drrrrghz4") == False
    assert is_good_password("344444hzji") == False
    assert is_good_password("*********") == False
    assert is_good_password("dfg$$$$$$") == False
    # Repeated characters should be allowed when not sequential
    assert is_good_password("2d2rf2g2t2") == True
    assert is_good_password("0s0nw0djy0dkeo0kdnfg0nd000nd0") == True
    # Passwords containing strings found in common passwords should fail
    assert is_good_password("iloveyoumikey") == False
    assert is_good_password("password1234") == False
    # Passwords over 15 characters can pass even if containing common passwords
    assert is_good_password("fksbzr§&fws*ilovemikeymouse") == True
    assert is_good_password("joeTesting067!") == True

