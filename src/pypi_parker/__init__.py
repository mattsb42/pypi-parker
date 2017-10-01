"""PyPI Parker setup expansion resources."""
import distutils.cmd
import os
import sys

from pypi_parker.config import load_config
from pypi_parker.build import generate_and_build_package

__version__ = '0.0.28'


class Park(distutils.cmd.Command):
    """Distutils Command for reading a :class:`pypi-parker` configuration
    and building distribution files for each name.
    """

    decription = 'Generates builds for all configured PyPI names'
    user_options = [
        ('park-config=', 'p', 'path to pypi-parker config file')
    ]

    def initialize_options(self) -> None:
        """Set default values for options."""
        self.park_config = 'park.cfg'

    def finalize_options(self) -> None:
        """Required by :class:`distutils.cmd` but not used."""
        self.park_config = os.path.abspath(self.park_config)

        if not os.path.isfile(self.park_config):
            sys.exit('Requested pypi_parker config file "{}" does not exist'.format(self.park_config))

    def run(self) -> None:
        """Run command."""
        base_dir = os.path.dirname(self.park_config)

        os.makedirs(os.path.join(base_dir, 'dist'), exist_ok=True)

        for package in load_config(self.park_config):
            generate_and_build_package(package, base_dir)
