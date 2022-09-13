from pathlib import Path
from io import BufferedReader

from typing import Union, List
from dataclasses import dataclass, field

from drivers.local.audio.base import BaseAudioReader
from drivers.local.text.base import BaseTextReader

from drivers.models.supported_audio_extensions import AudioExtensions
from drivers.models.supported_text_extensions import TextExtensions


@dataclass
class Reader:
    """ Interface to read local files with different file extensions.

    Usage:
        Reader(input_path=<particular_file_path>).read()
    """

    input_path: str = field(init=True)
    path_to_read: Path = field(init=False)

    file_extension: str = field(init=False)
    supported_extensions: List = field(default_factory=lambda:(TextExtensions.list() + AudioExtensions.list()))

    @staticmethod
    def _cast_str_to_path(path: str) -> Path:
        """ Helper method to cast input_path (str) to Path. """
        return Path(path)

    @staticmethod
    def _get_file_extension(path: Path) -> str:
        """ Helper method to get file extension. """
        return path.suffix.replace ('.', '')

    def __post_init__(self):
        self.path_to_read = self._cast_str_to_path(path=self.input_path)
        self.file_extension = self._get_file_extension(path=self.path_to_read)

    def file_exists(self) -> Union[bool, FileNotFoundError]:
        """ Function, which checks whether file exists at the given path. """

        if self.path_to_read.is_file():
            return True
        else:
            raise FileNotFoundError(f'Wrong path or file does not exist.')

    def correct_extension(self) -> Union[bool, OSError]:
        """ Function, which checks whether file extension match supported ones. """

        if self.file_extension in self.supported_extensions:
            return True
        else:
            raise OSError(f'File extension is not supported by the Reader. '
                          f'Supported ones are: {self.supported_extensions}')

    def read(self) -> Union[str, BufferedReader]:
        """ Entry point function, which reads file. """

        if self.file_exists() and self.correct_extension():
            if self.file_extension in TextExtensions.list():
                return BaseTextReader().read(path=self.path_to_read)
            else:
                return BaseAudioReader().read(path=self.path_to_read)