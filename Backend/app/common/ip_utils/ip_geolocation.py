import ipaddress
import logging
import requests

def is_public_ip(ip: str) -> bool:
    """
    Checks whether ip is in public range (i.e. can appear on the open internet). This means it is suitable for geolocation, abuse detection, rate limiting.
    Reserved IP addresses like "127.0.0.1" (localhost) cannot be geolocated meaningfully.

    More information on reserved ranges: https://en.wikipedia.org/wiki/Reserved_IP_addresses
    
    :param ip: ip adress of the client
    :type ip: str
    :return: True if ip is public, False otherwise
    :rtype: bool
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        return False
    
    if not ip_obj.is_global:
        logging.debug(f"IP issue: IP {ip} is not publicly routable (private, loopback, or reserved). Geolocation not possible.")
        return False
    
    return True
    

def geolocate_ip(client_ip: str) -> dict:
    """
    Locates the geo-origin of an IP address and returns a dictionary with the following keys: continent, country, country_code, and city. Should geolocation fail, the value assigned to the keys will be "N/A".

    --------
    **Fields overview**:

    :param client_ip: ip address of the client as a string

    --------
    **Example usage:**
    ```
    geo_location = geolocate_ip("127.0.0.1")
    geo_location ->  {
            "continent": "N/A",
            "country": "N/A", # 99% accurate
            "country_code": "N/A",
            "city": "N/A", # 83% accurate
            "isp": "N/A", # internet service provider: if not a consumer ISP → higher risk.
            "org": "N/A", # often similar to isp
            "as": "N/A", # Autonomous System (AS) number (id assigned to network)
            "asname": "N/A", # short BGP name for the autonomous system
            "proxy": "N/A", # if true, traffic routed via VPN/public proxy/anonymized service
            "hosting": "N/A", # if true, IP belongs to hosting or cloud provider → strong indication of automation
            "mobile": "N/A", # whether IP belongs to mobile carrier network
            }
    ```
    """
    res = {
        "continent": "N/A",
        "country": "N/A",
        "country_code": "N/A",
        "city": "N/A",
        "isp": "N/A", 
        "org": "N/A", 
        "as": "N/A", 
        "asname": "N/A", 
        "proxy": "N/A", 
        "hosting": "N/A", 
        "mobile": "N/A", 
    }
    if not client_ip or not is_public_ip(client_ip):
        return res
    
    # NOTE: read the docs at https://ip-api.com/docs/api:json
    fields = ",".join([
    "status",
    "message",
    "continent",
    "country",
    "countryCode",
    "city",
    "isp",
    "org",
    "as",
    "asname",
    "proxy",
    "hosting",
    "mobile",
    ])
    query_url = f"http://ip-api.com/json/{client_ip}?fields={fields}"

    try:
        ip_info_request = requests.get(query_url, timeout=5) #timeout after 5 seconds
        ip_info = ip_info_request.json()
    except Exception as e:
        logging.debug(f"IP geolocation error: Failed to get geolocation of IP {client_ip}. Error: {str(e)}")
        return res

    if not ip_info:
        logging.debug(f"IP geolocation error: Failed to get geolocation of IP {client_ip}.")
        return res

    if ip_info.get("status") != "success":
        logging.debug(f"IP geolocation error: Geolocation query failed. Message: {ip_info.get('message', 'N/A')}")
        return res

    res["continent"] = ip_info.get("continent", "N/A")
    res["country"] = ip_info.get("country", "N/A")
    res["country_code"] = ip_info.get("countryCode", "N/A")
    res["city"] = ip_info.get("city", "N/A")
    res["isp"] = ip_info.get("isp", "N/A")
    res["org"] = ip_info.get("org", "N/A")
    res["as"] = ip_info.get("as", "N/A")
    res["asname"] = ip_info.get("asname", "N/A")
    res["proxy"] = ip_info.get("proxy", "N/A")
    res["hosting"] = ip_info.get("hosting", "N/A")
    res["mobile"] = ip_info.get("mobile", "N/A")

    return res