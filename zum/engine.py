"""
The main module for the zum library.
"""

import json
from typing import Any, List, Optional

import httpx

from zum.configs.core import (
    retrieve_config_file,
    search_for_config_file,
    validate_configs,
)
from zum.configs.errors import InvalidConfigFileError, MissingConfigFileError
from zum.constants import DEFAULT_CONFIG_FILE_NAME
from zum.executor import execute
from zum.requests.core import generate_request
from zum.requests.validations import validate_raw_endpoint


class Engine:

    """
    Class to handle the overall behaviour of zum.
    """

    def __init__(self, config_file_name: str = DEFAULT_CONFIG_FILE_NAME) -> None:
        self.__output: Optional[str] = None
        self.__exception: Optional[Exception] = None

        try:
            search_for_config_file(config_file_name)
            configs = retrieve_config_file(config_file_name)
            validate_configs(configs)
        except (MissingConfigFileError, InvalidConfigFileError) as error:
            configs = {}
            self.__exception = error

        self.__metadata = configs.get("metadata", {})
        self.__endpoints = configs.get("endpoints", {})

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
        self._validate_configurations()
        validate_raw_endpoint(self.__endpoints[instruction])
        request = generate_request(self.__endpoints[instruction], arguments)
        response = execute(self.__metadata["server"], request)
        self.__handle_response(response)

    def _validate_configurations(self) -> None:
        """Validates that the configurations were correctly loaded."""
        if self.__exception:
            raise self.__exception

    def __handle_response(self, response: httpx.Response) -> None:
        """Handles the response."""
        try:
            self.__output = json.dumps(
                response.json(), indent=2, sort_keys=False, ensure_ascii=False
            )
        except TypeError:
            self.__output = response.text
