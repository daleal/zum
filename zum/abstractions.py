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
        self,
        route: str,
        method: str,
        params: Optional[List[str]] = None,
        body: Optional[List[str]] = None,
    ) -> None:
        self.route = route
        self.method = method
        self.params = params
        self.body = body

    def parse_params(self, options: List[Any]) -> Tuple[Dict[str, Any], List[Any]]:
        """
        Parse the options list into a params dictionary and
        the rest of the options list.
        """
        if self.params is None:
            return {}, options
        if len(options) < len(self.params):
            raise MissingEndpointParamsError(
                "Invalid amount of params passed to the command."
            )
        return (
            {x[0]: x[1] for x in zip(self.params, options)},
            options[len(self.params) :],
        )

    def parse_body(self, options: List[Any]) -> Tuple[Dict[str, Any], List[Any]]:
        """
        Parse the options list into a json body dictionary and
        the rest of the options list.
        """
        if self.body is None:
            return {}, options
        if len(options) < len(self.body):
            raise MissingEndpointParamsError(
                "Invalid amount of params passed to the command."
            )
        return (
            {x[0]: x[1] for x in zip(self.body, options)},
            options[len(self.body) :],
        )

    def get_route(self, **params: Any) -> str:
        """Interpolate params into the route."""
        return self.route.format(**params)


class Metadata:

    """
    Class to encapsulate the metadata information.
    """

    def __init__(self, server: str) -> None:  # pylint: disable=R0903
        self.server = server.rstrip("/")
