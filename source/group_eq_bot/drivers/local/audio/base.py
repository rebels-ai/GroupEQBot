from dataclasses import dataclass

from pathlib import Path
from io import BufferedReader


@dataclass
class BaseAudioReader:
    """ Interface to read files with audio extensions. """

    _READER_MODE = 'rb'

    def read(self, path: Path) -> BufferedReader:
        """ Function, which reads the audio file at specified path.

        Note:
            function will return BufferReader.
        """
        return open(path, self._READER_MODE)
