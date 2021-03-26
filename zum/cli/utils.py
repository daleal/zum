"""
A module to hold the zum CLI helpers.
"""

from argparse import ArgumentParser

from zum.constants import DEFAULT_CONFIG_FILE_NAME


def attach_file_flag(parser: ArgumentParser) -> None:
    """Attaches the --file flag to a parser."""
    # Add file flag
    parser.add_argument(
        "-f",
        "--file",
        dest="file",
        default=DEFAULT_CONFIG_FILE_NAME,
        help=f"config file name, defaults to '{DEFAULT_CONFIG_FILE_NAME}'",
    )
