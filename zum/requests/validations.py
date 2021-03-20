"""
Module for the requests validations of zum.
"""

from typing import Any, Dict

from zum.constants import HTTP_METHODS
from zum.requests.errors import InvalidEndpointDefinitionError


def validate_raw_endpoint(raw_endpoint: Dict[str, Any]) -> None:
    """Validates that the endpoint's dictionary data is valid."""
    validate_raw_endpoint_route(raw_endpoint)
    validate_raw_endpoint_method(raw_endpoint)


def validate_raw_endpoint_route(raw_endpoint: Dict[str, Any]) -> None:
    """Validates that the endpoint's dictionary route value is valid."""
    if "route" not in raw_endpoint:
        raise InvalidEndpointDefinitionError(
            "Missing 'route' attribute for the endpoint"
        )
    route = raw_endpoint["route"]
    if not isinstance(route, str):
        raise InvalidEndpointDefinitionError(
            "The 'route' attribute of the endpoint must be a string"
        )


def validate_raw_endpoint_method(raw_endpoint: Dict[str, Any]) -> None:
    """Validates that the endpoint's dictionary method value is valid."""
    if "method" not in raw_endpoint:
        raise InvalidEndpointDefinitionError(
            "Missing 'method' attribute for the endpoint"
        )
    method = raw_endpoint["method"]
    if not isinstance(method, str):
        raise InvalidEndpointDefinitionError(
            "The 'method' attribute for the endpoint must be a string"
        )
    if method.strip().lower() not in HTTP_METHODS:
        raise InvalidEndpointDefinitionError(
            "Invalid 'method' value for the endpoint (not a valid HTTP method)"
        )
