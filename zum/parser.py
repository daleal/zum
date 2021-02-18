"""
Module for the core parsing logic of zum.
"""

from typing import Any, Dict

import tomlkit

from zum.abstractions import Endpoint, Metadata
from zum.constants import DEFAULT_HTTP_METHOD
from zum.errors import InvalidConfigFileError


def parse_metadata(metadata: Dict[str, str]) -> Metadata:
    return Metadata(server=metadata["server"])


def parse_endpoints(endpoints: Dict[str, Any]) -> Dict[str, Endpoint]:
    return {name: parse_endpoint(endpoint) for name, endpoint in endpoints.items()}


def parse_endpoint(data: dict) -> Endpoint:
    return Endpoint(
        route=data["route"],
        method=data.get("method") or DEFAULT_HTTP_METHOD,
        params=data.get("params"),
        body=data.get("body"),
    )
