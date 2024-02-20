import logging
import requests

def geolocate_ip(client_ip):
    """
    geolocate_ip(ip_address: str) -> obj
    ------------------------------------------------------------
    Returns:
        An object with the following keys: continent, country, country_code, and city.
        Should geolocation fail, the value assigned to the keys will be "N/A".
    ------------------------------------------------------------
    Example usage:
    
    geo_location = geolocate_ip("127.0.0.1")
    geo_location ->  {
            "continent": "N/A",
            "country": "N/A",
            "country_code": "N/A",
            "city": "N/A"
        }
    """
    res = {
        "continent": "N/A",
        "country": "N/A",
        "country_code": "N/A",
        "city": "N/A"
    }
    
    # Localhost may use 127.0.0.0–127.255.255.255
    # Other reserved ranges: https://en.wikipedia.org/wiki/Reserved_IP_addresses
    if client_ip == "127.0.0.1":
        logging.debug(f"IP issue: IP 127.0.0.1 is reserved range. Actual IP could not be retrieved. Localhost address.")
        return res
    
    query_url = f"http://ip-api.com/json/{client_ip}?fields=status,message,continent,country,countryCode,city"

    try:
        ip_info_request = requests.get(query_url)
        ip_info = ip_info_request.json()
    except Exception as e:
        logging.debug(f"IP geolocation error: Failed to get geolocation of IP {client_ip}. Error: {str(e)}")
        return res

    if not ip_info:
        logging.debug(f"IP geolocation error: Failed to get geolocation of IP {client_ip}.")
        return res

    if ip_info and ip_info["status"] == "fail":
        logging.debug(f"IP geolocation error: Geolocation query failed. Message: {ip_info["message"]}")
        return res

    res["continent"] = ip_info["continent"] 
    res["country"] = ip_info["country"]
    res["country_code"] = ip_info["countryCode"]
    res["city"] = ip_info["city"]

    return res