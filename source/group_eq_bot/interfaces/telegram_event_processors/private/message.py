from dataclasses import dataclass

from telegram.ext import ContextTypes

from interfaces.models.internal_event.event import ExpectedInternalEvent
from utilities.internal_logger.logger import logger
from storage.schemas.bot_events.schema import Builder
from interfaces.telegram_event_handlers.conversation_update.commands.start import StartValidation


@dataclass
class MessageEventProcessor:
    """ Main Interface to process Private Messages Updates. """

    internal_event: ExpectedInternalEvent
    context: ContextTypes.DEFAULT_TYPE

    async def process(self):
        """
        Entrypoint to process Private Messages (ExpectedInternalEvent)
        event and write it to EventDrivenDatabase.
        """

        logger.info('[MessageEventProcessor] is called ...')
        logger.info('[MessageEventProcessor] attempting to write to storage ...')

        # document = Builder(object=self.internal_event).build()
        # document.schema.save(index=document.index_name)
