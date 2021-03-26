"""
A module to hold the zum CLI parser generators.
"""

from argparse import ArgumentParser
from typing import List

import zum
from zum.cli.utils import attach_file_flag


def generate_main_parser(
    config_file_name: str, actions_list: List[str]
) -> ArgumentParser:
    """Generates the main parser."""
    warning = (
        f"Beware! No config file was found with the name '{config_file_name}'!"
        if not actions_list
        else ""
    )

    # Create parser
    parser = ArgumentParser(
        description="Command line interface tool for zum.", epilog=warning
    )

    # Add file flag
    attach_file_flag(parser)

    # Add version flag
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"zum version {zum.__version__}",
    )

    if actions_list:
        # Add action argument
        parser.add_argument("action", choices=actions_list, nargs=1)

        # Add params
        parser.add_argument("params", nargs="*")

    return parser


def generate_config_file_parser() -> ArgumentParser:
    """Generates the proxy parser that processes the config file."""
    # Create parser
    parser = ArgumentParser(add_help=False)

    # Add file flag
    attach_file_flag(parser)

    return parser
