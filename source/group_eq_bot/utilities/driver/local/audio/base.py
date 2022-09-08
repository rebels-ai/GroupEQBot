from pathlib import Path


class BaseAudioReader:
    """
        Alternative:

        from pydub import AudioSegment
        audio = AudioSegment.from_file('file.m4a')
    """

    def open(path_to_read: Path) -> AudioObject:
        """  """
        return open(path_to_read, 'rb')
