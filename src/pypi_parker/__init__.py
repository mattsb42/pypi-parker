"""PyPI Parker setup expansion resources."""

import argparse
import importlib.metadata
import sys
from pathlib import Path

from pypi_parker.build import generate_and_build_package
from pypi_parker.config import load_config

__version__ = importlib.metadata.version(__name__)


def cli(args=None) -> None:
    """
    CLI entry point for pypi-parker.
    """
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(
        description="Generate placeholder packages from pypi-parker configuration.",
    )
    parser.add_argument(
        "-f",
        "--config-file",
        type=Path,
        default="park.cfg",
        required=False,
        help="Path to pypi-parker configuration file",
    )
    parser.add_argument("--version", action="version", version=__version__)

    args = parser.parse_args(args)

    if not args.config_file.is_file():
        parser.error(f'Configuration file "{args.config_file}" does not exist')

    base_dir = args.config_file.parent.resolve()
    for package in load_config(args.config_file.resolve()):
        generate_and_build_package(package, base_dir)
