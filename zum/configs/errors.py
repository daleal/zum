"""
A module to hold the custom exceptions for the zum library regarding the
configuration file.
"""


class MissingConfigFileError(Exception):
    """An exception for when the config file is missing."""


class InvalidConfigFileError(Exception):
    """An exception for when the config file is invalid."""
