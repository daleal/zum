"""
A module to route the zum CLI traffic.
"""

from typing import Any

from zum.cli.generators import generate_config_file_parser, generate_main_parser
from zum.engine import Engine
from zum.utils import log


def dispatcher(*args: Any, **kwargs: Any) -> None:
    """
    Main CLI method, recieves the command line action and dispatches it to
    the corresponding method.
    """
    config_file_name = get_config_file_name(*args, **kwargs)

    engine = Engine(config_file_name)

    parser = generate_main_parser(config_file_name, engine.actions)
    parsed_args = parser.parse_args(*args, **kwargs)

    engine.execute(parsed_args.action[0], parsed_args.params)  # pragma: nocover
    log(engine.output)  # pragma: nocover


def get_config_file_name(*args: Any, **kwargs: Any) -> str:
    """Creates the config file parser and extracts the config file name."""
    file_parser = generate_config_file_parser()

    file_parser_args, _ = file_parser.parse_known_args(*args, **kwargs)

    return file_parser_args.file
