from typing import Optional
from pydantic import BaseModel

from group_eq_bot.interfaces.models.chat import ChatType
from group_eq_bot.interfaces.models.event import EventType
from group_eq_bot.interfaces.models.member import MemberStatus
from group_eq_bot.interfaces.models.external_event import ExpectedExternalEvent


class ExpectedInternalEvent(BaseModel):
    """ Internal event data model definition. """

    class Config:
        extra = 'allow'
        arbitrary_types_allowed = True

    event: ExpectedExternalEvent
    event_type: EventType
    event_time: float  # datetime converted into POSIX timestamp

    chat_id: int
    chat_type: ChatType
    chat_name: str

    user_id: int
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    new_status: Optional[MemberStatus]
    old_status: Optional[MemberStatus]

    message_id: Optional[int]  # refer to router.router_helper.get_message_id
    message: Optional[str]

