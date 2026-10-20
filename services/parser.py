from urllib.parse import urlparse, urlsplit, parse_qs
from models.models import Strategy

def vless_uri_resolver(uri: str) -> Strategy:
    uri_parameters = urlsplit(uri)
    query_parameters = uri_parameters.query.split("&")
    
    parsed_query: dict[str, str] = dict(
        field.split("=", 1) for field in query_parameters
        if field
        )
        
    # Validate query fields with model fields
    fields_data: dict = Strategy.model_fields
    
    allowed_fields: set = set(fields_data.keys())
    allowed_aliases: set = {
        field.alias for field in fields_data.values()
        if field.alias 
        }
    # Operator "|" works as "+", but does not repeat elements
    ALLOWED = allowed_fields | allowed_aliases
    
    # Exclude allowed elements to get unknown fields
    unknown_fields: set = set(parsed_query.keys()) - ALLOWED
    if unknown_fields:
        raise ValueError(f"Unknown vless data fields: {unknown_fields}.")
    
    # Get uuid, resolve host as address and port  
    uuid, _, host = uri_parameters.netloc.partition("@")
    if not host:
        raise ValueError("Invalid vless uri: missing '@'.")
    address, _, port = host.partition(":")
    if not port:
        raise ValueError("Invalid vless uri: missing port.")
    label = uri_parameters.fragment or None

    strategy_data: dict[str, str | None] = {
        "uuid": uuid,
        "address": address,
        "port": port,
        **parsed_query,
        "label": label
    }
    return Strategy(**strategy_data)

