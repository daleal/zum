"""
Module for the core configuration logic of zum.
"""

from pathlib import Path
from typing import Any, Dict

import tomlkit

from zum.configs.errors import InvalidConfigFileError, MissingConfigFileError


def search_for_config_file(file_name: str) -> None:
    """Searches for the config file. If it doesn't exist, raises an error."""
    if not Path(file_name).is_file():
        raise MissingConfigFileError(f"Missing config file '{file_name}'.")


def retrieve_config_file(file_name: str) -> Dict[str, Any]:
    """Opens the config file and returns the parsed dictionary."""
    with open(file_name, "r") as raw_configs:
        configs = raw_configs.read()
    return tomlkit.parse(configs)


def validate_configs(configs: Dict[str, Any]) -> None:
    """Validate that the configs are not malformed."""
    validate_metadata(configs)
    validate_endpoints(configs)


def validate_metadata(configs: Dict[str, Any]) -> None:
    """Validate that the metadata key of the configs are not malformed."""
    if "metadata" not in configs:
        raise InvalidConfigFileError("Missing 'metadata' section of the config file")
    if not isinstance(configs["metadata"], dict):
        raise InvalidConfigFileError(
            "The 'metadata' section shold be a dictionary or mapping."
        )
    if "server" not in configs["metadata"]:
        raise InvalidConfigFileError(
            "Missing 'server' value from the 'metadata' section of the config file"
        )


def validate_endpoints(configs: Dict[str, Any]) -> None:
    """Validate that the endpoints key of the configs are not malformed."""
    if "endpoints" not in configs:
        raise InvalidConfigFileError("Missing 'endpoints' section of the config file")
    if not isinstance(configs["endpoints"], dict):
        raise InvalidConfigFileError(
            "The 'endpoints' section shold be a dictionary or mapping."
        )
    if len(list(configs["endpoints"].keys())) == 0:
        raise InvalidConfigFileError(
            "At least one endpoint is required on the config file"
        )
