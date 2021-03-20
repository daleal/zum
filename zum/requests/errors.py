"""
A module to hold the custom exceptions for the zum library regarding the
requests.
"""


class MissingEndpointParamsError(Exception):
    """An exception for when an incorrect amount of params is passed."""


class InvalidEndpointDefinitionError(Exception):
    """An exception for when an endpoint is defined incorrectly."""
