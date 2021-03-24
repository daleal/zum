"""
A module to hold the zum CLI helpers.
"""

from argparse import ArgumentParser
from typing import Optional

from zum.constants import DEFAULT_CONFIG_FILE_NAME


def log(data: Optional[str]) -> None:
    """Logs a string to the console."""
    print(data)


def attach_file_flag(parser: ArgumentParser) -> None:
    # Add file flag
    parser.add_argument(
        "-f",
        "--file",
        dest="file",
        default=DEFAULT_CONFIG_FILE_NAME,
        help=f"config file name, defaults to '{DEFAULT_CONFIG_FILE_NAME}'",
    )
