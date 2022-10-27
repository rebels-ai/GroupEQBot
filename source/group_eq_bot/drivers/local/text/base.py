from dataclasses import dataclass
from pathlib import Path


@dataclass
class BaseTextReader:
    """ Interface to read files with text extensions. """

    _READER_MODE = 'rt'

    def read(self, path: Path) -> str:
        """ Function, which reads the text from file at specified path. """

        with open(path, self._READER_MODE) as file:
            context = file.read()

        return context
