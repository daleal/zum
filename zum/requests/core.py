"""
Module for the core requests logic of zum.
"""

from json import load
from pathlib import Path
from typing import Any, Dict, List, NoReturn, Union

from zum.requests.errors import InvalidRequestBodyFileError
from zum.requests.helpers import reduce_arguments
from zum.requests.models import Request


def load_request_body(arguments: List[str]) -> Union[Dict[str, Any], NoReturn]:
    """
    Parse the JSON request body into a dictionary and return it if the
    specified file exists.
    """
    if len(arguments) >= 1:
        body_file: Path = Path(arguments.pop())
        if body_file.exists() and body_file.is_file():
            with body_file.open("r") as body_contents:
                return load(body_contents)

        else:
            if not body_file.exists():
                raise InvalidRequestBodyFileError(
                    f"Request body file located at '{body_file.absolute()}' does"
                    + " not exist!"
                )

            if not body_file.is_file():
                raise InvalidRequestBodyFileError(
                    f"Request body file located at '{body_file.absolute()}' is not"
                    + " a file!"
                )

    raise InvalidRequestBodyFileError(
        "Please provide the file path to the request body."
    )


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

    body: Dict[str, Any] = dict()
    if (
        raw_endpoint.get("body") is not None
        and isinstance(raw_endpoint.get("body"), str)
        and raw_endpoint.get("body") == "json"
    ):
        body = load_request_body(remaining_arguments)
    else:
        body, _ = reduce_arguments(raw_endpoint.get("body"), remaining_arguments)

    return Request(raw_endpoint["route"], raw_endpoint["method"], params, headers, body)
