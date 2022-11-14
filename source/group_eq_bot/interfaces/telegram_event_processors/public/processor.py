from dataclasses import dataclass
from telegram.ext import ContextTypes

from interfaces.models.internal_event.event_type import EventType
from interfaces.models.internal_event.event import ExpectedInternalEvent

from interfaces.telegram_event_processors.public.bot import BotEventProcessor
from interfaces.telegram_event_processors.public.message import MessageEventProcessor
from interfaces.telegram_event_processors.public.member import MemberEventProcessor

from utilities.internal_logger.logger import logger


@dataclass
class Processor:
    """ Public event processor interface, which stands for processing MESSAGE and MEMBER events. """

    internal_event: ExpectedInternalEvent
    context: ContextTypes.DEFAULT_TYPE

    async def handle(self) -> None:
        """ Entrypoint for public processor which handles  Message | Member events. """
        
        event_type = self.internal_event.event_type

        if event_type == EventType.message.value:
            logger.info('[PROCESSOR] Event type -- "MESSAGE" ')
            logger.info('[PROCESSOR] telegram_event_router to Public MessageEventProcessor ...')
            await MessageEventProcessor(internal_event=self.internal_event,
                                        context=self.context).process()

        elif event_type == EventType.member.value:
            logger.info('[PROCESSOR] Event type -- "MEMBER" ')
            logger.info('[PROCESSOR] telegram_event_router to Public MemberEventProcessor ...')
            await MemberEventProcessor(internal_event=self.internal_event,
                                       context=self.context).process()

        elif event_type == EventType.bot.value:
            logger.info('[PROCESSOR] Event type -- "BOT" ')
            logger.info('[PROCESSOR] telegram_event_router to Public BotEventProcessor ...')
            await BotEventProcessor(internal_event=self.internal_event,
                                    context=self.context).process()

        # @TODO:potentially implement --> elif  == EventType.button        
        else:
            logger.warning(f'[PROCESSOR] EventProcessor registered unknown EventType.'
                           f'{event_type}')
        return
