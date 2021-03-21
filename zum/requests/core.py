"""
Module for the core requests logic of zum.
"""

from typing import Any, Dict, List

from zum.requests.helpers import reduce_arguments
from zum.requests.models import Request


def generate_request(raw_endpoint: Dict[str, Any], arguments: List[str]) -> Request:
    """
    Given the raw endpoint data and the arguments list, generates a Request
    object with the data necessary to execute said request.
    """
    params, remaining_arguments = reduce_arguments(
        raw_endpoint.get("params"), arguments
    )
    headers, remaining_arguments = reduce_arguments(
        raw_endpoint.get("headers"), remaining_arguments
    )
    body, _ = reduce_arguments(raw_endpoint.get("body"), remaining_arguments)
    return Request(raw_endpoint["route"], raw_endpoint["method"], params, headers, body)
