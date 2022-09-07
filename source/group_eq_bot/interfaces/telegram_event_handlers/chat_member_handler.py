from dataclasses import dataclass
from telegram.ext import ChatMemberHandler

from group_eq_bot.interfaces.telegram_event_router.router import route_event


@dataclass
class MemberHandler:
    chat_member_types_to_apply = ChatMemberHandler.CHAT_MEMBER
    callback_to_call = route_event

    handler = ChatMemberHandler(chat_member_types=chat_member_types_to_apply,
                                callback=callback_to_call)