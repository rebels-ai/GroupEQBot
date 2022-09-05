from enum import Enum


class MemberStatus(Enum):
    """ Internal wrapper on ChatMember of telegram Update (TelegramEvent) definition used in ExpectedInternalEvent. """

    owner = 'creator'
    administrator = 'administrator'
    member = 'member'
    left = 'left'  # if user attempts to join the group
    restricted = 'restricted'
    banned = 'kicked'
    no_status = None
