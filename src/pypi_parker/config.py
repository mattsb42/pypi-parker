"""Tooling to generate package configurations from configuration files."""
import configparser
from typing import Dict, Iterator, Sequence, Union

__all__ = ('load_config',)
FALLBACK_VALUES = dict(
    classifiers=['Development Status :: 7 - Inactive'],
    description='parked using pypi-parker',
    long_description=(
        'This package has been parked either for future use or to protect against typo misdirection.\n'
        'If you believe that it has been parked in error, please contact the package owner.'
    )
)
STRING_LITERAL_KEYS = ('classifiers',)
SETUP_CONFIG = Dict[str, Union[str, Sequence[str]]]


def _string_literal_to_lines(string_literal: str) -> Sequence[str]:
    """Split a string literal into lines.

    :param string_literal: Source to split
    """
    return sorted([
        line.strip() for line
        in string_literal.strip().splitlines()
    ])


def _update_description(setup_base: SETUP_CONFIG) -> None:
    """Update description field with description keys if defined."""
    try:
        description_keys = _string_literal_to_lines(setup_base.pop('description_keys'))
        description_setup = {key: str(setup_base[key]) for key in description_keys}  # type: Dict[str, str]
    except KeyError:
        return

    for field in ('description', 'long_description'):
        try:
            setup_base[field] = str(setup_base[field]).format(**description_setup)
        except KeyError:
            pass


def _update_string_literal_values(setup_base: SETUP_CONFIG) -> None:
    """Update ``setup_base`` by splitting string literal key values into lines."""
    for key in STRING_LITERAL_KEYS:
        try:
            setup_base[key] = _string_literal_to_lines(str(setup_base[key]))
        except KeyError:
            pass


def _update_fallback_values(setup_base: SETUP_CONFIG) -> None:
    """Update ``setup_base`` with fallback values."""
    if 'long_description' not in setup_base and 'description' in setup_base:
        setup_base['long_description'] = setup_base['description']

    for key, value in FALLBACK_VALUES.items():
        if key not in setup_base:
            setup_base[key] = value


def _generate_setup(config: configparser.ConfigParser, name: str) -> SETUP_CONFIG:
    """Generate a ``setuptools.setup`` call for ``name`` from ``config``.

    :param config: Loaded parker config
    :param name: Package name for which to generate setup config
    """
    setup_base = {}  # type: SETUP_CONFIG
    if name in config:
        setup_base.update(dict(config[name].items()))
    else:
        setup_base.update(dict(config['DEFAULT'].items()))
    setup_base['name'] = name

    if name in config:
        setup_base.update(config[name].items())

    _update_description(setup_base)
    _update_string_literal_values(setup_base)
    _update_fallback_values(setup_base)

    if len(str(setup_base['description']).splitlines()) > 1:
        raise ValueError('Package "description" must be a single line.')

    return setup_base


def load_config(filename: str) -> Iterator[SETUP_CONFIG]:
    """Load ``parker.conf`` and generate all ``setuptools.setup`` calls.

    :param filename: Filename of configuation file to load
    """
    config = configparser.ConfigParser()
    config.read(filename)

    names = config.sections()
    if 'names' in config:
        names.remove('names')
        names.extend([
            name for name in config['names']
            if name not in names and name not in config['DEFAULT']
        ])

    for name in names:
        yield _generate_setup(config, name)
