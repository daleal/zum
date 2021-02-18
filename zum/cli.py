"""
A module to route the CLI traffic.
"""

import sys

from argparse import ArgumentParser, _SubParsersAction
from typing import Any, List

import zum
from zum.executor import Executor


def dispatcher(*args: Any, **kwargs: Any) -> None:
    """
    Main CLI method, recieves the command line action and dispatches it to
    the corresponding method.
    """
    executor = Executor()
    actions_list = list(executor.endpoints.keys())

    parser = generate_parser(actions_list)
    parsed_args = parser.parse_args(*args, **kwargs)

    try:
        if parsed_args.action in actions_list:
            executor.execute(parsed_args.action)
        else:
            print("Invalid action.")
            parser.print_help()
            sys.exit(1)
    except AttributeError:
        print("An argument is required for the zum command.")
        parser.print_help()
        sys.exit(1)


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

    # Create subparsers
    subparsers = parser.add_subparsers(help="Action to be executed.")

    # Populate subparsers
    for action in actions_list:
        generate_subparser(subparsers, action)

    return parser


def generate_subparser(subparsers: _SubParsersAction, action: str) -> ArgumentParser:
    parser = subparsers.add_parser(action)
    parser.set_defaults(action=action)
    return parser
