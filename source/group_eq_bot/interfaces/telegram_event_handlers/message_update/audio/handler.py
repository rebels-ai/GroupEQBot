from dataclasses import dataclass
from telegram.ext import MessageHandler, filters

from interfaces.telegram_event_router.router import route_event


@dataclass
class AudioMessageHandler:
    """ Handler builder for audio message updates """
    filters_to_apply = filters.AUDIO | filters.VOICE
    callback_to_call = route_event

    handler = MessageHandler(filters=filters_to_apply,
                             callback=callback_to_call)
