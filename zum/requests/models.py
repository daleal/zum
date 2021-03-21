"""
A module to hold the models for the zum library regarding the requests.
"""

from typing import Any, Dict


class Request:

    """
    Class to encapsulate the request structure.
    """

    def __init__(
        self,
        route: str,
        method: str,
        params: Dict[str, str],
        headers: Dict[str, str],
        body: Dict[str, Any],
    ) -> None:
        self._route = route
        self.method = method
        self.params = params
        self.headers = headers
        self.body = body

    @property
    def route(self) -> str:
        """Interpolate params into the route."""
        return self._route.format(**self.params)
