"""PyPI Parker setup expansion resources."""
# virtualenv + distutils bug in pylint: https://github.com/PyCQA/pylint/issues/73
from distutils.cmd import Command  # pylint: disable=import-error,no-name-in-module
import os
import sys

from pypi_parker.build import generate_and_build_package
from pypi_parker.config import load_config

__version__ = '0.1.2'


class Park(Command):
    """Distutils Command for reading a :class:`pypi-parker` configuration
    and building distribution files for each name.
    """

    decription = 'Generates builds for all configured PyPI names'
    user_options = [
        ('park-config=', 'p', 'path to pypi-parker config file')
    ]

    def initialize_options(self) -> None:
        """Set default values for options."""
        self.park_config = 'park.cfg'  # pylint: disable=attribute-defined-outside-init

    def finalize_options(self) -> None:  # noqa=D401
        """Required by :class:`distutils.cmd` but not used."""
        self.park_config = os.path.abspath(self.park_config)  # pylint: disable=attribute-defined-outside-init

        if not os.path.isfile(self.park_config):
            sys.exit('Requested pypi_parker config file "{}" does not exist'.format(self.park_config))

    def run(self) -> None:
        """Run command."""
        base_dir = os.path.dirname(self.park_config)

        for package in load_config(self.park_config):
            generate_and_build_package(package, base_dir)
