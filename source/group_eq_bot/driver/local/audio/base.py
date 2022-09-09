from io import BufferedReader
from pathlib import Path


class BaseAudioReader:

    @staticmethod
    def open(path_to_read: Path) -> BufferedReader:
        return open(path_to_read, 'rb')
