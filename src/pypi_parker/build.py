""""""
import glob
import os
import shutil
import subprocess
import sys
import tempfile

import attr

from pypi_parker.config import SETUP_CONFIG
from pypi_parker.util import SpecificTemporaryFile

__all__ = ('generate_and_build_package',)
ALLOWED_SETUP_SUFFIXES = ('setup.py sdist', 'setup.py check -r -s')


def _setup_body(setup_conf: SETUP_CONFIG) -> str:
    """Generate the setup.py body given a setup config.

    .. note::

        The setup.py generated here will raise an ImportError for every actions
        except for those whitelisted for use when building the package.

    :param dict setup_conf: Setup config for which to generate setup.py
    :rtype: str
    """
    return os.linesep.join([
        'import sys',
        'from setuptools import setup',
        '',
        "args = ' '.join(sys.argv).strip()",
        'if not any(args.endswith(suffix) for suffix in [{allowed_suffixes}]):',
        '    raise {error}',
        '',
        'setup(',
        '    {config}',
        ')',
        ''
    ]).format(
        error=repr(ImportError(setup_conf['description'])),
        config=',{linesep}    '.join([
            '{}= {}'.format(key, repr(value))
            for key, value
            in setup_conf.items()
        ]).format(linesep=os.linesep),
        allowed_suffixes=', '.join(repr(each) for each in ALLOWED_SETUP_SUFFIXES)
    )


def generate_and_build_package(package_config: SETUP_CONFIG, origin_directory: str) -> None:
    """Generates, validates, and builds a package using the specified configuration and places
    the resulting distributable files in ``{origin_directory}/dist``.

    :param dist package_config: Package setup configuration
    :param str origin_directory: Filepath to desired base output directory
    """

    with tempfile.TemporaryDirectory() as tmpdirname:

        os.chdir(tmpdirname)

        setup_py = SpecificTemporaryFile(
            name=os.path.join(tmpdirname, 'setup.py'),
            body=_setup_body(package_config)
        )

        manifest_in = SpecificTemporaryFile(
            name=os.path.join(tmpdirname, 'MANIFEST.in'),
            body='include setup.py'
        )

        with setup_py, manifest_in:
            validate_command = [sys.executable, setup_py.name, 'check', '-r', '-s']
            subprocess.check_call(validate_command)

            build_command = [sys.executable, setup_py.name, 'sdist']
            subprocess.check_call(build_command)

        for file in glob.glob(os.path.join(tmpdirname, 'dist/*')):
            shutil.copy(file, os.path.join(origin_directory, 'dist'))

        os.chdir(origin_directory)
