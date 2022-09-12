from enum import Enum
from typing import List


class AudioExtensions(Enum):
    """ Audio file extensions Telegram can accept in a send/reply functions"""
    mp4 = 'm4a'
    mp3 = 'mp3'
    ogg = 'ogg'

    @classmethod
    def list(cls) -> List:
        return list(map(lambda c: c.value, cls))
