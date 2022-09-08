from enum import Enum


class SupportedFilesExtensions(Enum):
    """ File extensions Telegram can accept in a send/reply functions"""
    audio = 'm4a'
    text = 'txt'
