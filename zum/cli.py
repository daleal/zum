"""
A module to route the zum CLI traffic.
"""

from argparse import ArgumentParser
from typing import Any, List

import zum
from zum.core import Executor


def dispatcher(*args: Any, **kwargs: Any) -> None:
    """
    Main CLI method, recieves the command line action and dispatches it to
    the corresponding method.
    """
    executor = Executor()
    actions_list = list(executor.endpoints.keys())

    parser = generate_parser(actions_list)
    parsed_args = parser.parse_args(*args, **kwargs)

    executor.execute(parsed_args.action[0], parsed_args.params)


def generate_parser(actions_list: List[str]) -> ArgumentParser:
    """Generates the action parser."""
    # Create parser
    parser = ArgumentParser(description="Command line interface tool for zum.")

    # Add version command
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"zum version {zum.__version__}",
    )

    # Add action argument
    parser.add_argument("action", choices=actions_list, nargs=1)

    # Add params
    parser.add_argument("params", nargs="*")

    return parser
