"""
A module for containing the endpoint logic of zum.
"""


class Endpoint:

    """
    Class to encapsulate an endpoint.
    """

    def __init__(self, route: str, method: str):
        self.route = route
        self.method = method
