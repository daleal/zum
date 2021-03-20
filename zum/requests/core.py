"""
Module for the core requests logic of zum.
"""

from typing import Any, Dict, List, Optional, Tuple

from zum.requests.errors import MissingEndpointParamsError
from zum.requests.models import Request


def generate_request(raw_endpoint: Dict[str, Any], arguments: List[str]) -> Request:
    """
    Given the raw endpoint data and the arguments list, generates a Request
    object with the data necessary to execute said request.
    """
    params, remaining_arguments = reduce_arguments(
        raw_endpoint.get("params"), arguments
    )
    body, _ = reduce_arguments(raw_endpoint.get("body"), remaining_arguments)
    return Request(raw_endpoint["route"], raw_endpoint["method"], params, body)


def reduce_arguments(
    keys: Optional[List[str]], arguments: List[Any]
) -> Tuple[Dict[str, Any], List[Any]]:
    """
    Given a :keys array of strings, maps the first :keys.length elements
    of the :arguments array to the :keys elements as keys, returning the
    mapped elements and the rest of the :arguments array.
    """
    if keys is None:
        return {}, arguments
    if len(arguments) < len(keys):
        raise MissingEndpointParamsError(
            "Invalid amount of arguments passed to the command."
        )
    return (
        {x[0]: x[1] for x in zip(keys, arguments)},
        arguments[len(keys) :],
    )
