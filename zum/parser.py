"""
Module for the core parsing logic of zum.
"""

from typing import Any, Dict

from zum.abstractions import Endpoint, Metadata
from zum.constants import DEFAULT_HTTP_METHOD


def parse_metadata(metadata: Dict[str, str]) -> Metadata:
    """Parse the metadata into a Metadata object."""
    return Metadata(server=metadata["server"])


def parse_endpoints(endpoints: Dict[str, Any]) -> Dict[str, Endpoint]:
    """Parse all the endpoints."""
    return {name: parse_endpoint(endpoint) for name, endpoint in endpoints.items()}


def parse_endpoint(data: dict) -> Endpoint:
    """Parse an endpoint's data into an Endpoint object."""
    return Endpoint(
        route=data["route"],
        method=data.get("method") or DEFAULT_HTTP_METHOD,
        params=data.get("params"),
        body=data.get("body"),
    )
