"""
A module for containing the abstractions of the zum library.
"""

from typing import Any, Dict, List, Optional, Tuple

from zum.errors import MissingEndpointParamsError


class Endpoint:

    """
    Class to encapsulate an endpoint.
    """

    def __init__(
        self, route: str, method: str, params: Optional[List[str]] = None
    ) -> None:
        self.route = route
        self.method = method
        self.params = params

    def parse_params(self, options: List[Any]) -> Tuple[Dict[str, Any], List[Any]]:
        if self.params is None:
            return {}, options
        if len(options) < len(self.params):
            raise MissingEndpointParamsError(
                "Invalid amount of params passed to the command."
            )
        return (
            {x[0]: x[1] for x in zip(self.params, options)},
            options[len(self.params):]
        )

    def get_route(self, **params: Any) -> str:
        return self.route.format(**params)


class Metadata:

    """
    Class to encapsulate the metadata information.
    """

    def __init__(self, server: str) -> None:
        self.server = server.rstrip("/")
