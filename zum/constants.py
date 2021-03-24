"""
A module to hold all the constants for the zum library.
"""


# Config file
DEFAULT_CONFIG_FILE_NAME = "zum.toml"

# Endpoints
DEFAULT_HTTP_METHOD = "get"

# HTTP related
HTTP_METHODS = [
    "get",
    "put",
    "post",
    "delete",
    "options",
    "head",
    "patch",
    "trace",
]

# Request body value types
REQUEST_BODY_VALUE_TYPES = ["string", "integer", "float", "boolean", "null"]
