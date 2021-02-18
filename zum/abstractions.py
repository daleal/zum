"""
A module for containing the abstractions of zum.
"""


class Endpoint:

    """
    Class to encapsulate an endpoint.
    """

    def __init__(self, route: str, method: str) -> None:
        self.route = route
        self.method = method


class Metadata:

    """
    Class to encapsulate the metadata information.
    """

    def __init__(self, server: str) -> None:
        self.server = server.rstrip("/")
