from typing import Any, Dict

from zum.errors import InvalidConfigFileError


def validate_metadata(configs: Dict[str, Any]) -> None:
    if "metadata" not in configs:
        raise InvalidConfigFileError("Missing 'metadata' section of the config file")
    if "server" not in configs["metadata"]:
        raise InvalidConfigFileError(
            "Missing 'server' value from the 'metadata' section"
        )


def validate_endpoints(configs: Dict[str, Any]) -> None:
    if "endpoints" not in configs:
        raise InvalidConfigFileError("Missing 'endpoints' section of the config file")
    if len(configs["endpoints"]) == 0:
        raise InvalidConfigFileError("At least one endpoint is required")


def validate_configs(configs: Dict[str, Any]) -> None:
    validate_metadata(configs)
    validate_endpoints(configs)
