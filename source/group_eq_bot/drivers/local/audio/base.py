from io import BufferedReader
from pathlib import Path


class BaseAudioReader:
    """ Reader for audio files """

    @staticmethod
    def read(path_to_read: Path) -> BufferedReader:
        """ Function, which reads the audio file at specified path """
        return open(path_to_read, 'rb')
