"""
A module to hold all the validation methods for the zum library.
"""

from typing import Any, Dict

from zum.errors import InvalidConfigFileError


def validate_metadata(configs: Dict[str, Any]) -> None:
    """Validate that the metadata key of the config file is not malformed."""
    if "metadata" not in configs:
        raise InvalidConfigFileError("Missing 'metadata' section of the config file")
    if "server" not in configs["metadata"]:
        raise InvalidConfigFileError(
            "Missing 'server' value from the 'metadata' section"
        )


def validate_endpoints(configs: Dict[str, Any]) -> None:
    """Validate that the endpoints key of the config file is not malformed."""
    if "endpoints" not in configs:
        raise InvalidConfigFileError("Missing 'endpoints' section of the config file")
    if len(configs["endpoints"]) == 0:
        raise InvalidConfigFileError("At least one endpoint is required")


def validate_configs(configs: Dict[str, Any]) -> None:
    """Validate that the config file is not malformed."""
    validate_metadata(configs)
    validate_endpoints(configs)
