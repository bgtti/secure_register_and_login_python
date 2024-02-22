import ipaddress
import logging

# Why use a function for ip validation:
# request.remote_addr may return 127.0.0.1
# this happens when running Flask locally or deployed otherwise behind a proxy
# this problem might be solved by getting the client's ip from the request headers: X-Forwarded-For or X-Real-IP
# now, this can make the application vulnerable to IP spoofing
# you can read more about this issue here: https://esd.io/blog/flask-apps-heroku-real-ip-spoofing.html
# added ip validation to dimish the risk 

def get_client_ip(request):
    """
    get_client_ip(request: object) -> str | None
    ---------------------------------------------
    Returns:
        Client's IP (str) if format is valid.
        None if IP address could not be verified.
    ---------------------------------------------
    Example usage:

    from flask import request
    # ...inside route:
    get_client_ip(request) -> "192.168.1.100"

    # or...
    get_client_ip(request) -> None
    """
    # Check if the request is behind a proxy
    if request.headers.getlist("X-Forwarded-For"):
        ip_list = [ip.strip() for ip in request.headers["X-Forwarded-For"].split(",")]
        ip = ip_list[0]
    else:
        ip = request.remote_addr

    if ip == "127.0.0.1":
        logging.debug(f"IP issue: IP 127.0.0.1 is reserved range. Actual IP could not be retrieved.")
        return "127.0.0.1"
    
    else:
        try:
            ipaddress.ip_address(ip)
            return ip
        except ValueError as e:
            logging.warning(f"IP error: IP address could not be verified. Error: {e}")
            return None