from dataclasses import dataclass

from telegram.ext import ContextTypes
from group_eq_bot.interfaces.models.internal_event import ExpectedInternalEvent

from group_eq_bot.storage.interfaces.documents.event import EventsDatabaseEventInterface
from group_eq_bot.storage.interfaces.documents.chat import EventsDatabaseChatInterface
from group_eq_bot.storage.interfaces.documents.user import EventsDatabaseUserInterface

from group_eq_bot.utilities.internal_logger.logger import logger


@dataclass
class MessageEventProcessor:
    """ Main Interface to process Messages Updates. """

    internal_event: ExpectedInternalEvent
    context: ContextTypes.DEFAULT_TYPE

    async def process(self):
        """
        Entrypoint to process  Public | Private Message (ExpectedInternalEvent)
        event and write it to EventDrivenDatabase.
        """

        logger.info('[MessageEventProcessor] is called ...')
        logger.info('[MessageEventProcessor] attempting to write to storage ...')

        EventsDatabaseEventInterface(internal_event=self.internal_event).process()
        EventsDatabaseChatInterface(internal_event=self.internal_event).process()
        EventsDatabaseUserInterface(internal_event=self.internal_event).process()
