"""
The main module for the zum library.
"""

import json
from typing import Any, Dict, List, Optional

import httpx

from zum.configs.core import (
    retrieve_config_file,
    search_for_config_file,
    validate_configs,
)
from zum.constants import CONFIG_FILE_NAME
from zum.executor import execute
from zum.requests.core import generate_request
from zum.requests.validations import validate_raw_endpoint


class Engine:

    """
    Class to handle the overall behaviour of zum.
    """

    def __init__(self) -> None:
        search_for_config_file(CONFIG_FILE_NAME)
        configs = retrieve_config_file(CONFIG_FILE_NAME)
        validate_configs(configs)
        self.__metadata = configs["metadata"]
        self.__endpoints = configs["endpoints"]
        self.__output: Optional[str] = None

    @property
    def output(self) -> Optional[str]:
        """Returns the internal state of the output."""
        return self.__output

    @property
    def actions(self) -> List[str]:
        """Returns a list with the possible actions."""
        return list(self.__endpoints.keys())

    def execute(self, instruction: str, arguments: List[Any]) -> None:
        """
        Executes the main zum logic.
        """
        validate_raw_endpoint(self.__endpoints[instruction])
        request = generate_request(self.__endpoints[instruction], arguments)
        response = execute(self.__metadata["server"], request)
        self.__handle_response(response)

    def __handle_response(self, response: httpx.Response) -> None:
        """Handles the response."""
        try:
            self.__output = json.dumps(
                response.json(), indent=2, sort_keys=False, ensure_ascii=False
            )
        except TypeError:
            self.__output = response.text
