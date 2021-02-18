"""
A module to hold the custom exceptions for the zum library.
"""


class InvalidConfigFileError(Exception):
    """An exception for when the config file is invalid or missing."""


class MissingEndpointParamsError(Exception):
    """An exception for when an incorrect amount of params is passed."""
