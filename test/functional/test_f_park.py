"""Functional test suite for :class:`pypi_parker.cli`."""

import os
import shlex

import pytest

from pypi_parker import cli

from .functional_helpers import HERE, TEST_PACKAGE_NAMES, read


@pytest.mark.parametrize(
    "config_filename, args",
    (
        ("park.cfg", ""),
        ("A_DIFFERENT_FILENAME", "--config-file A_DIFFERENT_FILENAME"),
        ("ANOTHER_FILENAME", " -f ANOTHER_FILENAME"),
    ),
)
def test_park(tmpdir, config_filename, args):
    target_dir = tmpdir.mkdir("test")
    target_config = target_dir.join(config_filename)
    target_config.write(read(os.path.join(HERE, "vectors", "park.cfg")))

    os.chdir(str(target_dir))

    cli(shlex.split(args))

    results = os.listdir(os.path.join(str(target_dir), "dist"))
    assert len(results) == len(TEST_PACKAGE_NAMES)


def test_park_file_not_found_default(tmpdir):
    target_dir = tmpdir.mkdir("test")
    target_setup = target_dir.join("setup.py")
    target_setup.write("from setuptools import setup\nsetup()\n")

    os.chdir(str(target_dir))

    with pytest.raises(SystemExit):
        cli(args=[])


def test_park_file_not_found_custom_filename(tmpdir):
    target_dir = tmpdir.mkdir("test")
    target_config = target_dir.join("park.cfg")
    target_config.write(read(os.path.join(HERE, "vectors", "park.cfg")))

    os.chdir(str(target_dir))

    with pytest.raises(SystemExit):
        cli(args=["--park-config", "ANOTHER_FILENAME"])
