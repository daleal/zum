"""Module for the core parsing logic of zum."""

from typing import Dict

import tomlkit

from zum.parser.endpoints import Endpoint
from zum.parser.utils import parse_endpoint


class Parser:

    """
    Class to encapsulate the parsing logic.
    """

    def __init__(self) -> None:
        self.metadata: Dict[str, str] = {}
        self.endpoints: Dict[str, Endpoint] = {}

    @staticmethod
    def __get_raw_data() -> dict:
        with open("zum.toml") as raw_data:
            data = raw_data.read()
        return tomlkit.parse(data)

    def parse(self) -> None:
        data = self.__get_raw_data()
        for name, endpoint in data["endpoints"].items():
            self.endpoints[name] = parse_endpoint(endpoint)
