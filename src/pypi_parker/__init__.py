"""PyPI Parker setup expansion resources."""
import importlib.metadata
import sys
import argparse
from pathlib import Path

from pypi_parker.build import generate_and_build_package
from pypi_parker.config import load_config

__version__ = importlib.metadata.version(__name__)


def cli() -> None:
    parser = argparse.ArgumentParser(
        description='Generate placeholder packages from pypi-parker configuration.',
    )
    parser.add_argument(
        '-f', '--config-file',
        type=Path,
        default='park.cfg',
        required=False,
        help='Path to pypi-parker configuration file',
    )
    parser.add_argument('--version', action='version', version=__version__)

    args = parser.parse_args(sys.argv[1:])

    if not args.config_file.is_file():
        parser.error('Configuration file "{}" does not exist'.format(args.config_file))

    base_dir = args.config_file.parent.resolve()
    for package in load_config(args.config_file.resolve()):
        generate_and_build_package(package, base_dir)
