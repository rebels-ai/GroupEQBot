from dataclasses import dataclass
from pathlib import Path

from driver.local.audio.base import BaseAudioReader
from driver.local.text.base import BaseTextReader
from driver.models.supported_extensions import  SupportedFilesExtensions


@dataclass
class Reader:
    path: Path  # full path to a particular file to open

    def check_path_exists(self) -> None:
        """  """

        try:
            path_exists = self.path.exists()
        except NotFoundError:
            raise f'{self.path} does not exist. Check configurations.'

        return 

    def check_file_extension_match_supported_ones(self) -> None:
        """  """

        extension = self.path.suffix  # idea to get the extension (without “.”)
        extension_hits = True if extension in SupportedFilesExtensions else False

        if extension_hits:
            return 
        else:
            raise NotFoundError(f'File extension is not supported by the reader. Supported ones are: {SupportedFilesExtensions}')  

    def get_file_extension(self) -> str:
        """  """
        return self.path.suffix  # idea to get the extension (without “.”)

    def open(self):
        """  """
        self.check_path_exists()
        self.check_file_extension_match_supported_ones()

        file_extension = self.get_file_extension()

        if file_extension == SupportedFilesExtensions.audio:
            return BaseAudioReader().open(path_to_open=self.path)
        else:
            return BaseTextReader().open(path_to_open=self.path)
