from urllib.parse import urlparse, urlsplit, parse_qs
from models.models import Strategy

vless_strategy_uri: str = "vless://18f72be7-0651-4037-928b-8a309d685796@194.107.126.157:443?security=reality&encryption=none&pbk=qFBIVGsvXTMeJcdJz6GiL7DG0XNhCg7rItza7t0qTgU&fp=chrome&sni=google.com&sid=9eb31eb7572c0882&flow=xtls-rprx-vision&type=tcp#MyVLESS"

def vless_uri_resolver(uri: str) -> Strategy:
    uri_parameters = urlsplit(uri)
    query_parameters = uri_parameters.query.split("&")
    
    parsed_query: dict[str, str] = dict(
        parameter.split("=", 1) for parameter in query_parameters if parameter
        )
        
    uuid, _, host = uri_parameters.netloc.partition("@")
    if not host:
        raise ValueError("Invalid vless URI: missing '@'.")
    address, _, port = host.partition(":")
    label = uri_parameters.fragment

    strategy_data: dict[str, str | None] = {
        "uuid": uuid,
        "address": address,
        "port": port,
        **parsed_query,
        "label": label
    }
    return Strategy(**strategy_data)

