from dataclasses import dataclass
from telegram.ext import ContextTypes

from interfaces.models.internal_event.event_type import EventType
from interfaces.models.internal_event.event import ExpectedInternalEvent
from interfaces.telegram_event_processors.private.bot import BotEventProcessor

from utilities.internal_logger.logger import logger


@dataclass
class Processor:

    internal_event: ExpectedInternalEvent
    context: ContextTypes.DEFAULT_TYPE

    async def handle(self) -> None:
        logger.info('[PROCESSOR] is called.')

        event_type = self.internal_event.event_type

        if event_type == EventType.bot.value:
            logger.info('[PROCESSOR] Event type -- "BOT" ')
            logger.info('[PROCESSOR] telegram_event_router to Private BotEventProcessor ...')
            await BotEventProcessor(internal_event=self.internal_event,
                                    context=self.context).process()
     
        else:
            logger.warning(f'[PROCESSOR] EventProcessor registered unknown EventType.'
                           f'{event_type}')
        logger.info('[PROCESSOR] finished.')

        return
