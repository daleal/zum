"""
The main module of the zum library.
"""

import json
from typing import Any, Dict, List

import httpx

from zum.parser import parse_endpoints, parse_metadata
from zum.utils import read_config_file
from zum.validations import validate_configs


class Executor:
    def __init__(self) -> None:
        configs = read_config_file()
        validate_configs(configs)
        self.metadata = parse_metadata(configs["metadata"])
        self.endpoints = parse_endpoints(configs["endpoints"])

    def execute(self, instruction: str, options: List[Any]) -> None:
        endpoint = self.endpoints[instruction]
        params, remaining_options = endpoint.parse_params(options)
        body, remaining_options = endpoint.parse_body(remaining_options)
        url = f"{self.metadata.server}{endpoint.get_route(**params)}"
        response = self.query(url, endpoint.method, body)
        self.handle_response(response)

    @staticmethod
    def query(url: str, method: str, body: Dict[str, Any]) -> httpx.Response:
        return httpx.request(method, url, json=body)

    @staticmethod
    def handle_response(response: httpx.Response) -> None:
        view = json.dumps(
            response.json(), indent=2, sort_keys=False, ensure_ascii=False
        )
        print(view)
