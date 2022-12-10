from enum import Enum
from typing import List


class TextExtensions(Enum):
    """ Text file extensions Telegram can accept in a send/reply functions"""
    txt = 'txt'

    @classmethod
    def list(cls) -> List:
        return list(map(lambda c: c.value, cls))
