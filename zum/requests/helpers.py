"""
Module for the requests helpers of zum.
"""

from typing import Any, Dict, List, Optional, Tuple, Union

from zum.requests.errors import (
    InvalidBodyParameterTypeError,
    MissingEndpointParamsError,
)
from zum.requests.validations import validate_body_parameter_definition


def reduce_arguments(
    keys: Optional[List[str]], arguments: List[Any]
) -> Tuple[Dict[str, Any], List[Any]]:
    """
    Given a :keys array of strings, maps the first :keys.length elements
    of the :arguments array to the :keys elements as keys, returning the
    mapped elements and the rest of the :arguments array.
    """
    if keys is None:
        return {}, arguments
    if len(arguments) < len(keys):
        raise MissingEndpointParamsError(
            "Invalid amount of arguments passed to the command."
        )
    casted_params = [cast_parameter(*x) for x in zip(keys, arguments)]
    return (
        # The next line is equivalent to `{**param for param in casted_params}`
        {key: value for param in casted_params for key, value in param.items()},
        arguments[len(keys) :],
    )


def cast_parameter(
    definition: Union[str, Dict[str, str]], value: str
) -> Dict[str, Any]:
    """
    Casts a value to its parameter definition and returns a dictionary with the
    required key name and the value casted to its right type.
    """
    validate_body_parameter_definition(definition)
    if isinstance(definition, str):
        return {definition: value}
    if "type" not in definition:
        return {definition["name"]: value}
    try:
        return {definition["name"]: cast_value(value, definition["type"])}
    except ValueError:
        raise InvalidBodyParameterTypeError(  # pylint: disable=W0707
            f"Parameter '{value}' can't be casted to '{definition['type']}'"
        )


def cast_value(value: str, casting_type: str) -> Any:
    """Casts value depending on the casting type."""
    if casting_type == "integer":
        return int(value)
    if casting_type == "float":
        return float(value)
    if casting_type == "boolean":
        if value not in ["true", "false"]:
            raise InvalidBodyParameterTypeError(
                f"Booleans can't be '{value}', only 'true' or 'false'"
            )
        return value == "true"
    if casting_type == "null":
        if value != "null":
            raise InvalidBodyParameterTypeError(
                f"Null parameters can't be '{value}', only 'null'"
            )
        return None
    return value  # String
