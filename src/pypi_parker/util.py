"""Utility helpers for :class:`pypi_parker.Park`."""
import os
from typing import Any

__all__ = ('SpecificTemporaryFile',)


class SpecificTemporaryFile(object):  # pylint: disable=too-few-public-methods
    """Context manager for temporary files with a known desired name and body.

    :param name: Filename of file to create
    :param body: Data to write to file
    """

    def __init__(self, name: str, body: str) -> None:
        """Initialize parameters."""
        self.name = name
        self.body = body

    def _write_file(self) -> None:
        """Write the requested body to the requested file."""
        with open(self.name, 'w') as file:
            file.write(self.body)

    def _delete_file(self) -> None:
        """Delete the created file."""
        os.remove(self.name)

    def __enter__(self):
        # type: () -> SpecificTemporaryFile
        """Create the specified file and write the body on enter."""
        self._write_file()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """Clean up the created file."""
        self._delete_file()
