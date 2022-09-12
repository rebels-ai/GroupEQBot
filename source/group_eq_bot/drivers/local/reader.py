from dataclasses import dataclass
from typing import Union
from pathlib import Path
from io import BufferedReader

from drivers.local.audio.base import BaseAudioReader
from drivers.local.text.base import BaseTextReader
from drivers.models.supported_audio_extensions import AudioExtensions
from drivers.models.supported_text_extensions import TextExtensions


@dataclass
class Reader:
    """ Files reader from specified path """

    path: Path

    def __post_init__(self):
        self.path = Path(self.path)

    def file_exists(self):
        """ Function, which checks whether file exists at the given path"""

        if not self.path.is_file():
            raise FileNotFoundError(f'{self.path} is a wrong path or file does not exist')

    def extension_supported(self, extension: str) -> bool:
        """ Function, which checks whether file extention mathches supported ones """

        available_extensions = TextExtensions.list() + AudioExtensions.list()
        if extension in available_extensions:
            return True
        else:
            raise OSError(f'File extension is not supported by the reader. Supported ones are: {available_extensions}')

    def get_file_extension(self) -> str:
        """ Function, which returns file extension without dot """
        return self.path.suffix.replace('.', '')

    def read(self) -> Union[str, BufferedReader]:
        """ Function, which opens the file, depending on the extension """

        self.file_exists()
        file_extension = self.get_file_extension()
        self.extension_supported(file_extension)

        text_extension = True if file_extension in TextExtensions.list() else False

        return BaseTextReader().read(path_to_read=self.path) if text_extension else BaseAudioReader().read(path_to_read=self.path)
