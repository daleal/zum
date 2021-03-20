"""
The main module of the zum library.
"""

import json
from typing import Any, Dict, List

import httpx

from zum.configs.core import (
    retrieve_config_file,
    search_for_config_file,
    validate_configs,
)
from zum.constants import CONFIG_FILE_NAME
from zum.requests.core import generate_request
from zum.requests.validations import validate_raw_endpoint


class Executor:

    """
    Class to encapsulate the execution flow of a request.
    """

    def __init__(self) -> None:
        search_for_config_file(CONFIG_FILE_NAME)
        configs = retrieve_config_file(CONFIG_FILE_NAME)
        validate_configs(configs)
        self.metadata = configs["metadata"]
        self.endpoints = configs["endpoints"]

    def execute(self, instruction: str, arguments: List[Any]) -> None:
        """
        Execute the query corresponding to the instruction using the arguments to
        generate the URL params and json body.
        """
        validate_raw_endpoint(self.endpoints[instruction])
        raw_endpoint = self.endpoints[instruction]
        request = generate_request(raw_endpoint, arguments)
        url = f"{self.metadata['server']}{request.route}"
        response = self.query(url, request.method, request.body)
        self.handle_response(response)

    @staticmethod
    def query(url: str, method: str, body: Dict[str, Any]) -> httpx.Response:
        """Queries the API."""
        return httpx.request(method, url, json=body)

    @staticmethod
    def handle_response(response: httpx.Response) -> None:
        """Show the response."""
        view = json.dumps(
            response.json(), indent=2, sort_keys=False, ensure_ascii=False
        )
        print(view)
