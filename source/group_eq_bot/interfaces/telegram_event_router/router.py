from telegram.ext import ContextTypes
from telegram import Update as TelegramEvent

from interfaces.models.chat import ChatType
from interfaces.telegram_event_validator.validator import EventValidator

from interfaces.telegram_event_processors.public.processor import Processor as PublicEventProcessor
from interfaces.telegram_event_processors.private.processor import Processor as PrivateEventProcessor

from utilities.internal_logger.logger import logger

CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE


async def route_event(event: TelegramEvent, context: CONTEXT_DEFAULT_TYPE) -> None:
    """ Entrypoint to `route` any incoming TelegramEvent either to public or to private event processors. """

    logger.info('[ROUTER] New Event Registered.')
    event = EventValidator(external_event=event).validated_internal_event
    logger.info('[ROUTER] New Event Validated and Casted in ExpectedInternalEvent.')

    if event.chat_type == ChatType.public:
        logger.info('[ROUTER] ChatType -- "PUBLIC" ')
        logger.info('[ROUTER] Routing to PublicEventProcessor ...')
        await PublicEventProcessor(internal_event=event,
                                   context=context).handle()

    elif event.chat_type == ChatType.private:
        logger.info('[ROUTER] ChatType -- "PRIVATE" ')
        logger.info('[ROUTER] Routing to PrivateEventProcessor ...')
        PrivateEventProcessor(internal_event=event,
                              context=context).handle()
    else:
        logger.warning(f'[ROUTER] Registered unknown ChatType.'
                       f'{event.chat_type}')

    return
