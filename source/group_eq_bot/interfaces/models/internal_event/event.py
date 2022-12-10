from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from interfaces.models.internal_event.chat_type import ChatType
from interfaces.models.internal_event.event_type import EventType
from interfaces.models.internal_event.member_status import MemberStatus
from interfaces.models.external_event.event import ExpectedExternalEvent


class ExpectedInternalEvent(BaseModel):
    """ Internal event data model definition. """

    class Config:
        extra = 'allow'
        arbitrary_types_allowed = True

    event: ExpectedExternalEvent
    event_type: str
    event_time: datetime  # datetime converted into POSIX timestamp

    chat_id: int
    chat_type: str
    chat_name: str

    user_id: int
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    new_status: Optional[str]
    old_status: Optional[str]

    message_id: Optional[int]  # refer to router.router_helper.get_message_id
    message: Optional[str]

