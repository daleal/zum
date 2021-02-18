import json
from typing import Any

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

    def execute(self, instruction: str, **kwargs: Any) -> None:
        url = f"{self.metadata.server}{self.endpoints[instruction].route}"
        method = self.endpoints[instruction].method
        response = self.query(url, method)
        self.handle_response(response)

    @staticmethod
    def query(url: str, method: str) -> httpx.Response:
        return httpx.request(method, url)

    @staticmethod
    def handle_response(response: httpx.Response) -> None:
        view = json.dumps(
            response.json(), indent=2, sort_keys=False, ensure_ascii=False
        )
        print(view)
