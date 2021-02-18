"""
A module to hold some utilities for the zum library.
"""

from typing import Any, Dict

import tomlkit

from zum.constants import CONFIG_FILE_NAME


def read_config_file() -> Dict[str, Any]:
    """Read and parse the config file."""
    with open(CONFIG_FILE_NAME, "r") as raw_configs:
        configs = raw_configs.read()
    return tomlkit.parse(configs)
