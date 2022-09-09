from enum import Enum
from typing import List


class SupportedFilesExtensions(Enum):
    """ File extensions Telegram can accept in a send/reply functions"""

    text = 'txt'
    audio_m4a = 'm4a'
    audio_mp3 = 'mp3'
    audio_ogg = 'ogg'

    @classmethod
    def list(cls) -> List:
        return list(map(lambda c: c.value, cls))