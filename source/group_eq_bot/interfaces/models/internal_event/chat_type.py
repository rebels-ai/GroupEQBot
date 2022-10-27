from enum import Enum


class ChatType(Enum):
    """ Internal wrapper on ChatType of telegram Update (TelegramEvent) definition used in ExpectedInternalEvent. """

    private = 'private'
    public = 'supergroup'
