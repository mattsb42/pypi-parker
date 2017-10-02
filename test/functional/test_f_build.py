"""Functional test suite for ``pypi_parker.config``."""
import os

import pytest

from pypi_parker import build

from .functional_helpers import (
    read_manifest_from_sdist, read_setup_config, read_setup_from_sdist,
    read_setup_py, TEST_PACKAGE_NAMES
)


@pytest.mark.parametrize('name', TEST_PACKAGE_NAMES)
def test_setup_body(name):
    setup_config = read_setup_config(name)

    assert build._setup_body(setup_config) == read_setup_py(name)


@pytest.mark.parametrize('name', TEST_PACKAGE_NAMES)
def test_generate_and_build_pacakge(tmpdir, name):
    target_dir = tmpdir.mkdir('test')
    setup_config = read_setup_config(name)

    build.generate_and_build_package(
        package_config=setup_config,
        origin_directory=str(target_dir)
    )

    assert os.path.isdir(os.path.join(str(target_dir), 'dist'))
    dist_contents = os.listdir(os.path.join(str(target_dir), 'dist'))
    assert len(dist_contents) == 1
    sdist_file = os.path.join(str(target_dir), 'dist', dist_contents[0])
    assert read_manifest_from_sdist(sdist_file) == build.MANIFEST
    assert read_setup_from_sdist(sdist_file) == read_setup_py(name)
