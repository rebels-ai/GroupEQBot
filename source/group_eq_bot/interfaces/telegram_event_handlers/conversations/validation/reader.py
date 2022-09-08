from dataclasses import dataclass
from pathlib import PurePath, Path
from io import BufferedReader
from typing import Union

from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra

from utilities.internal_logger.logger import logger

# Fetch bot configuration with hydra compose api
# https://hydra.cc/docs/advanced/compose_api/
initialize(version_base="1.2", config_path="../../../../configurations", job_name="question_reader")
configurations = compose(config_name="configuration")
GlobalHydra.instance().clear()


@dataclass
class Reader:
    file_path: str

    available_audio_extensions = ['.ogg', '.m4a', '.mp3']

    def read_question_file(self) -> Union[str, BufferedReader]:
        """ Function, which reads question file, using path from configurations """

        file_path = PurePath(self.file_path)
        file_extension = file_path.suffix

        if file_extension == '.txt':
            with open(self.file_path, 'rt') as file:
                question = file.read()
            return question

        elif file_extension in self.available_audio_extensions:
            question = open(self.file_path, 'rb')
            return question

        else:
            logger.warning('[READER] Got unexpected file extension')
