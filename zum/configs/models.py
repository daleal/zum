"""
A module to hold the models for the zum library regarding the configs.
"""

from typing import List, Optional

from zum.configs.types import ConfigElement
from zum.constants import DEFAULT_HTTP_METHOD


class Metadata:
    def __init__(self, server: str):
        self.server = server


class Endpoint:
    def __init__(
        self,
        name: str,
        route: str,
        http_method: str = DEFAULT_HTTP_METHOD,
        params: Optional[List[str]] = None,
        headers: Optional[List[ConfigElement]] = None,
        body: Optional[List[ConfigElement]] = None,
    ):
        self.name = name
        self.route = route
