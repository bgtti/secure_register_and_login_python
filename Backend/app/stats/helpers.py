import ipaddress
import logging

def anonymize_ip(ip_address):
    """
    anonymize_ip(ip_address: str) -> str
    ------------------------------------------------------------
    Returns:
        Anonymized IP as a string if input is a valid IP format.
        None if IP address is invalid or not v4/v6.
    ------------------------------------------------------------
    Example usage:
    
    anonymous_IPv4 = anonymize_ip("192.168.1.100")
    print("anonymous_IPv4") -> "192.168.1.0"

    anonymous_IPv6 = anonymize_ip("2001:db8::1")
    print("anonymous_IPv6") -> "2000000:db8::0000"
    """
    try:
        # Parse the IP address
        ip = ipaddress.ip_address(ip_address)

        # Truncate the last octet for IPv4, or the last 32 bits for IPv6
        if ip.version == 4:
            anonymized_ip = ".".join(str(octet) for octet in ip.packed[:-1]) + ".0"
        elif ip.version == 6:
            anonymized_ip = str(ip).replace(str(ip).split(':')[-1], '0000')
        else:
            raise ValueError("Unsupported IP version")
        return anonymized_ip
    except ipaddress.AddressValueError as e:
        logging.debug(f"Stats error: IP address could not be anonymized due to invalid IP address. Error: {e}")
        return None
    except ValueError as e:
        logging.debug(f"Stats error: IP address could not be anonymized due to unsuported IP version. Error: {e}")
        return None