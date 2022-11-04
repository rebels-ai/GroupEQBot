from dataclasses import dataclass
from telegram.ext import ChatMemberHandler

from interfaces.telegram_event_router.router import route_event


@dataclass
class BotHandler:
    chat_member_types_to_apply = ChatMemberHandler.MY_CHAT_MEMBER
    callback_to_call = route_event

    handler = ChatMemberHandler(chat_member_types=chat_member_types_to_apply,
                                callback=callback_to_call)