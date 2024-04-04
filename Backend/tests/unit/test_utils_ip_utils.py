from flask import request
import requests_mock
from app.utils.ip_utils.ip_address_validation import get_client_ip
from app.utils.ip_utils.ip_geolocation import geolocate_ip 
from app.utils.ip_utils.ip_anonymization import anonymize_ip

def test_get_client_ip(app_test):
    """
    GIVEN a request object
    CHECK whether ip address can be retrieved appropriately
    """
    # Test 1: without proxy
    with app_test.test_request_context(environ_base={"REMOTE_ADDR": "192.168.1.100"}):
        result = get_client_ip(request)
    assert result == "192.168.1.100"
    # Test 2: with proxy
    with app_test.test_request_context(headers={"X-Forwarded-For": "192.168.1.200, 10.0.0.1"}):
        result = get_client_ip(request)
    assert result == "192.168.1.200"
    # Test 3: with invalid ip
    with app_test.test_request_context(environ_base={"REMOTE_ADDR": "1"}):
        result = get_client_ip(request)
    assert result is None
    # Test 3: with reserved ip
    with app_test.test_request_context(environ_base={"REMOTE_ADDR": "127.0.0.1"}):
        result = get_client_ip(request)
    assert result == "127.0.0.1"

def test_anonymize_ip():
    """
    GIVEN an IP address
    CHECK whether the anonymize_ip function correctly anonymizes it
    """
    # Test 1: with a valid IPv4 address
    result_ipv4 = anonymize_ip("192.168.1.100")
    assert result_ipv4 == "192.168.1.0"

    # Test 2: with a valid IPv6 address
    result_ipv6 = anonymize_ip("2001:db8::1")
    assert result_ipv6 == "2000000:db8::0000"

    # Test 3: with an invalid IP address
    result_invalid = anonymize_ip("invalid_ip")
    assert result_invalid is None

def test_geolocate_ip():
    client_ip = "192.168.1.1"
    mock_url = f"http://ip-api.com/json/{client_ip}?fields=status,message,continent,country,countryCode,city"

    # Test 1: Simulate a successful response
    with requests_mock.Mocker() as m:
        expected_response = {
        "status": "success",
        "continent": "Asia",
        "country": "Japan",
        "countryCode": "JP",  
        "city": "Tokyo"
        }
        m.get(mock_url, json=expected_response)

        result = geolocate_ip(client_ip)

        assert result["continent"] == expected_response["continent"]
        assert result["country"] == expected_response["country"]
        assert result["country_code"] == expected_response["countryCode"] 
        assert result["city"] == expected_response["city"]

    # Test 2: Simulate a failure response (server error)
    with requests_mock.Mocker() as m:
        m.get(mock_url, status_code=500)

        result = geolocate_ip(client_ip)

    expected_result = {
        "continent": "N/A",
        "country": "N/A",
        "country_code": "N/A",
        "city": "N/A"
    }

    assert result == expected_result