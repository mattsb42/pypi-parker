"""Functional test suite for ``pypi_parker.config``."""
import os

import pytest

from pypi_parker import config

from .functional_helpers import HERE, read_raw_config, read_setup_config, TEST_PACKAGE_NAMES


def test_string_literal_to_lines():
    source = '''
    c
    a
    b
    a b c
    '''
    result = ['a', 'a b c', 'b', 'c']
    assert config._string_literal_to_lines(source) == result


@pytest.mark.parametrize('name', TEST_PACKAGE_NAMES)
def test_generate_setup(name):
    parser = read_raw_config()

    generated_setup = config._generate_setup(parser, name)

    assert generated_setup == read_setup_config(name)


@pytest.mark.parametrize('name', TEST_PACKAGE_NAMES)
def test_load_config(name):
    loaded_configs = [i for i in config.load_config(os.path.join(HERE, 'vectors', 'park.cfg'))]

    assert read_setup_config(name) in loaded_configs


def test_load_config_newline_in_description():
    with pytest.raises(ValueError) as excinfo:
        [i for i in config.load_config(os.path.join(HERE, 'vectors', 'bad_description.cfg'))]

    excinfo.match(r'Package "description" must be a single line.')
