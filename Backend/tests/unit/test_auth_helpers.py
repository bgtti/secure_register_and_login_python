from app.routes.auth.auth_helpers import anonymize_email, is_good_password

# def split_at_last_at(string):
#     part1, part2 = string.rsplit('@', 1)
#     return part1, part2

# def test_split():
#     assert split_at_last_at("jj@h.kkk") == ("jj", "h.kkk")
#     assert split_at_last_at("sddd@dd@ff.k") == ("sddd@dd", "ff.k")

def test_anonymize_email():
    """
    GIVEN an email
    CHECK that it anonymizes it correctly
    WHILE allowing for a wide variety of standards
    """
    # Basic email structure
    assert anonymize_email("john@mail.com") == "j***@m***.com" 
    # Emails containing punctuation 
    assert anonymize_email("john-smith@fakemail.com") == "j***-*****@f*******.com" 
    assert anonymize_email("john.+smith@fakemail.com") == "j***.+*****@f*******.com"
    # Emails with classic domains
    assert anonymize_email("johnSmith@fakemail.de") == "j********@f*******.de"
    assert anonymize_email("jsmith.designs@some-university.edu") == "j*****.*******@s***-**********.edu"
    # Emails with compound domains
    assert anonymize_email("sJohn@mail.com.br") == "s****@m***.***.br"
    assert anonymize_email("John.Smith@email.co.uk") == "J***.*****@e****.**.uk"
    assert anonymize_email("John.Smith@email.something.somethingelse.kfc") == "J***.*****@e****.*********.*************.kfc"
    # Emails with no domain
    assert anonymize_email("sJohn@mail") == "s****@m***"
    assert anonymize_email("s@m") == "s@m"
    # Emails with numbers
    assert anonymize_email("john123@fakemail.com") == "j******@f*******.com"
    # Emails with non-english letters
    assert anonymize_email("johnçöäü@fakemail.com") == "j*******@f*******.com"

def test_is_good_password():
    """
    GIVEN a password
    CHECK whether it meets the criteria for a safe password
    WHILE making it possible for user to use a great range of characters
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
    # Password can contain spaces and wide range of characters
    assert is_good_password("I followed the mouse in the park.") == True
    assert is_good_password("3%&/()=@{]üäà+-`*ç+") == True

