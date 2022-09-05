from enum import Enum


class EventType(Enum):
    """ Internal wrapper on EventType of telegram Update (TelegramEvent) definition used in ExpectedInternalEvent. """

    message = 'message'  # Public | Private Message update
    member = 'chat_member'  # Public Member status update
    private_with_bot = 'my_chat_member'  # Public | Private who-is-bot status update
