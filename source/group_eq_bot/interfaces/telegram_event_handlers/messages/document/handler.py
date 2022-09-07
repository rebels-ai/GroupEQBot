from dataclasses import dataclass
from telegram.ext import MessageHandler, filters

from group_eq_bot.interfaces.telegram_event_router.router import route_event


@dataclass
class DocumentMessageHandler:
    filters_to_apply = filters.Document.ALL
    callback_to_call = route_event

    handler = MessageHandler(filters=filters_to_apply,
                             callback=callback_to_call)