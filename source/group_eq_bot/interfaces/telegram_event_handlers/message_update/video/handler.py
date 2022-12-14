from dataclasses import dataclass
from telegram.ext import MessageHandler, filters

from interfaces.telegram_event_router.router import route_event


@dataclass
class VideoMessageHandler:
    """ Handler builder for video, animation and stickers message updates """
    filters_to_apply = filters.VIDEO | filters.VIDEO_NOTE | filters.Sticker.ALL | filters.ANIMATION | filters.PHOTO
    callback_to_call = route_event

    handler = MessageHandler(filters=filters_to_apply,
                             callback=callback_to_call)