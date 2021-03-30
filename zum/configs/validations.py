from typing import List, Optional

from zum.configs.errors import InvalidConfigFileError
from zum.configs.types import ConfigElement
from zum.constants import HTTP_METHODS


def validate_http_method(http_method: str, endpoint_name: str) -> None:
    if http_method not in HTTP_METHODS:
        raise InvalidConfigFileError(
            f"Invalid HTTP method '{http_method}' for endpoint '{endpoint_name}'"
        )


def validate_params(
    params: Optional[List[str]], route: str, endpoint_name: str
) -> None:
    if params is None:
        return

    if not all(map(lambda x: isinstance(x, str), params)):
        raise InvalidConfigFileError(
            f"Invalid param type for endpoint '{endpoint_name}' "
            "(params should be strings)"
        )
    for param in params:
        if f"{{{param}}}" not in route:
            raise InvalidConfigFileError(
                f"Param '{param}' isn't present on the route "
                f"for endpoint '{endpoint_name}'"
            )


def validate_headers(
    headers: Optional[List[ConfigElement]], endpoint_name: str
) -> None:
    if headers is None:
        return

    if not all(map(lambda x: isinstance(x, str), headers)):
        raise InvalidConfigFileError(
            f"Invalid header type for endpoint '{endpoint_name}' "
            "(headers should be strings)"
        )


def validate_body(body: Optional[List[ConfigElement]], endpoint_name: str) -> None:
    pass
