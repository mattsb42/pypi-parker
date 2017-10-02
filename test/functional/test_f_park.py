"""Functional test suite for :class:`pypi_parker.Park`."""
import os
import shlex
import subprocess
import sys

import pytest

from .functional_helpers import HERE, read, TEST_PACKAGE_NAMES


@pytest.mark.parametrize('config_filename, suffix', (
    ('park.cfg', ''),
    ('A_DIFFERENT_FILENAME', ' --park=A_DIFFERENT_FILENAME'),
    ('ANOTHER_FILENAME', ' -p ANOTHER_FILENAME')
))
def test_park(tmpdir, config_filename, suffix):
    target_dir = tmpdir.mkdir('test')
    target_setup = target_dir.join('setup.py')
    target_setup.write('from setuptools import setup\nsetup()\n')
    target_config = target_dir.join(config_filename)
    target_config.write(read(os.path.join(HERE, 'vectors', 'park.cfg')))

    os.chdir(str(target_dir))

    command_string = 'setup.py park' + suffix
    subprocess.check_call([sys.executable] + shlex.split(command_string))

    results = os.listdir(os.path.join(str(target_dir), 'dist'))
    assert len(results) == len(TEST_PACKAGE_NAMES)


def test_park_file_not_found_default(tmpdir):
    target_dir = tmpdir.mkdir('test')
    target_setup = target_dir.join('setup.py')
    target_setup.write('from setuptools import setup\nsetup()\n')

    os.chdir(str(target_dir))

    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_call([sys.executable, 'setup.py', 'park'])


def test_park_file_not_found_custom_filename(tmpdir):
    target_dir = tmpdir.mkdir('test')
    target_setup = target_dir.join('setup.py')
    target_setup.write('from setuptools import setup\nsetup()\n')
    target_config = target_dir.join('park.cfg')
    target_config.write(read(os.path.join(HERE, 'vectors', 'park.cfg')))

    os.chdir(str(target_dir))

    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_call([sys.executable, 'setup.py', 'park', '--park-config', 'ANOTHER_FILENAME'])
