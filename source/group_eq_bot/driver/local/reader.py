from dataclasses import dataclass
from pathlib import Path

from driver.local.audio.base import BaseAudioReader
from driver.local.text.base import BaseTextReader
from driver.models.supported_extensions import  SupportedFilesExtensions


@dataclass
class Reader:
    path: Path  # full path to a particular file to open

    def __post_init__(self) -> None:
        self.path = Path(self.path)

    def check_file_existance(self) -> None:
        """ Function, which checks whether file exist in given path and is a file """

        if not self.path.exists():
            raise FileNotFoundError(f'{self.path} path does not exist')
        if not self.path.is_file():
            raise FileNotFoundError(f'{self.path} is not a file')

    def matches_supported_extensions(self, file_extension) -> None:
        """ Function, which checks whether file extention mathches supported ones """

        available_extensions = SupportedFilesExtensions.list()
        if file_extension in available_extensions:
            return
        else:
            raise FileNotFoundError(f'File extension is not supported by the reader. Supported ones are: {SupportedFilesExtensions.list()}')  

    def get_file_extension(self) -> str:
        """ Function, which returns file extension without dot """
        return self.path.suffix.replace('.', '')

    def open(self):
        """ Function, which opens the file, depending on the extension """

        self.check_file_existance()
        file_extension = self.get_file_extension()
        self.matches_supported_extensions(file_extension)

        if file_extension == SupportedFilesExtensions.text.value:
            return BaseTextReader().open(path_to_read=self.path)
        else:
            return BaseAudioReader().open(path_to_read=self.path)
