from dataclasses import dataclass

from telegram.ext import ContextTypes

from interfaces.models.internal_event.event_type import EventType
from interfaces.models.internal_event.event import ExpectedInternalEvent
from interfaces.telegram_event_processors.private.bot import BotEventProcessor

from utilities.internal_logger.logger import logger


@dataclass
class Processor:
    """ Private event processor interface, which stands for processing BOT events. """

    internal_event: ExpectedInternalEvent
    context: ContextTypes.DEFAULT_TYPE

    async def handle(self) -> None:
        """ Entrypoint for private processor which handles Bot events. """

        logger.info('[Private Processor] is called.')
 
        event_type = self.internal_event.event_type

        if event_type == EventType.bot.value:
            logger.info('[Private Processor] Event type -- "BOT" ')
            logger.info('[Private Processor] telegram_event_router to Private BotEventProcessor ...')
            await BotEventProcessor(internal_event=self.internal_event,
                                    context=self.context).process()

        else:
            logger.warning(f'[Private Processor] registered unknown EventType.'
                           f'{event_type}')

        return
