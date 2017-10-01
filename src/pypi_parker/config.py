""""""
import configparser
from typing import Dict, Iterator, Sequence, Union

__all__ = ('load_config',)
FALLBACK_VALUES = dict(
    classifiers=['Development Status :: 7 - Inactive'],
    description=(
        'This package has been parked either for future use or to protect against typo misdirection.'
        ' If you believe that it has been parked in error, please contact the package owner.'
    )
)
LIST_LITERAL_KEYS = ('classifiers',)
SETUP_CONFIG = Dict[str, Union[str, Sequence[str]]]


def _string_literal_to_lines(string_literal: str) -> Sequence[str]:
    """Split a string literal into lines.

    :param str string_literal: Source to split
    :rtype: list of str
    """
    return [
        line.strip() for line
        in string_literal.split()
    ]


def _generate_setup(config: configparser.ConfigParser, name: str) -> SETUP_CONFIG:
    """Generate a ``setuptools.setup`` call for ``name`` from ``config``.

    :param config: Loaded parker config
    :type config: configparser.ConfigParser
    :param str name:
    """
    setup_base = {}  # type: SETUP_CONFIG
    if name in config:
        setup_base.update(dict(config[name].items()))
    else:
        setup_base.update(dict(config['DEFAULT'].items()))
    setup_base['name'] = name

    if name in config:
        setup_base.update(config[name].items())

    try:
        description_keys = _string_literal_to_lines(setup_base.pop('description_keys'))
        description_setup = {key: str(setup_base[key]) for key in description_keys}  # type: Dict[str, str]
        setup_base['description'] = str(setup_base['description']).format(**description_setup)
    except KeyError:
        pass

    for key in LIST_LITERAL_KEYS:
        try:
            setup_base[key] = _string_literal_to_lines(str(setup_base[key]))
        except KeyError:
            pass

    for key, value in FALLBACK_VALUES.items():
        if key not in setup_base:
            setup_base[key] = value

    if 'long_description' not in setup_base:
        setup_base['long_description'] = setup_base['description']

    return setup_base


def load_config(filename: str) -> Iterator[SETUP_CONFIG]:
    """Load ``parker.conf`` and generate all ``setuptools.setup`` calls."""
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