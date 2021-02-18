"""Module for the parsing utilities of zum."""

from zum.parser.endpoints import Endpoint


def parse_endpoint(data: dict) -> Endpoint:
    return Endpoint(route=data["endpoint"], method=data["method"])
