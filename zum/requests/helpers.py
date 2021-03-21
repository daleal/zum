"""
Module for the requests helpers of zum.
"""

from typing import Any, Dict, List, Optional, Tuple

from zum.requests.errors import MissingEndpointParamsError


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
