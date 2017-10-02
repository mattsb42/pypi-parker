"""Functional test suite for :class:`pypi_parker.util.SpecificTemporaryFile`."""
import base64
import os

from pypi_parker import util


def test_specific_temporary_file(tmpdir):
    filename = tmpdir.mkdir('test').join('a_file.txt')
    body = str(base64.b64encode(os.urandom(1024)))

    assert not os.path.exists(str(filename))

    with util.SpecificTemporaryFile(name=filename, body=body):
        assert os.path.isfile(str(filename))
        assert filename.read() == body

    assert not os.path.exists(str(filename))
