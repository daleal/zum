from typing import Any, Dict

import tomlkit

from zum.constants import CONFIG_FILE_NAME


def read_config_file() -> Dict[str, Any]:
    with open(CONFIG_FILE_NAME, "r") as raw_configs:
        configs = raw_configs.read()
    return tomlkit.parse(configs)
