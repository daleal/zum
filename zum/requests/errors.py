"""
A module to hold the custom exceptions for the zum library regarding the
requests.
"""


class MissingEndpointParamsError(Exception):
    """An exception for when an incorrect amount of params is passed."""


class InvalidEndpointDefinitionError(Exception):
    """An exception for when an endpoint is defined incorrectly."""


class InvalidBodyParameterTypeError(Exception):
    """
    An exception for when a body parameter tries to be casted to a
    type that doesn't match its intrinsec type.
    """


class InvalidRequestBodyFileError(Exception):
    """
    An exception used for any errors related to a JSON file provided as the
    body of a request.
    """
