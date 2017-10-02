"""Helper functions for ``pypi_parker`` functional tests."""
import codecs
import configparser
import json
import os
import tarfile

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PACKAGE_NAMES = (
    'my-test-package',
    'another-test-package',
    'testpackage-reloaded'
)


def read(filename):
    with open(filename) as f:
        return f.read()


def read_raw_config(filename=None):
    if filename is None:
        filename = os.path.join(HERE, 'vectors', 'park.cfg')
    parser = configparser.ConfigParser()
    parser.read(filename)
    return parser


def read_setup_config(name):
    return json.loads(read(os.path.join(HERE, 'vectors', name + '.setup')))


def read_setup_py(name):
    return read(os.path.join(HERE, 'vectors', name + '.setup.py'))


def read_file_from_sdist(sdist_filename, target_filename):
    with tarfile.open(sdist_filename, 'r') as sdist:
        for name in sdist.getnames():
            if name.endswith(target_filename) and name.count(os.path.sep) == 1:
                member = sdist.getmember(name)
                with sdist.extractfile(member) as target:
                    return target.read()


def read_setup_from_sdist(sdist_filename):
    return codecs.decode(read_file_from_sdist(sdist_filename, 'setup.py'), 'utf-8')


def read_manifest_from_sdist(sdist_filename):
    return codecs.decode(read_file_from_sdist(sdist_filename, 'MANIFEST.in'), 'utf-8')
