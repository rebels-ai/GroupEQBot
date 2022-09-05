from dataclasses import dataclass

from telegram.ext import ContextTypes
from models.internal_event import ExpectedInternalEvent

from databases.events_driven_database.interfaces.documents.event import EventsDatabaseEventInterface
from databases.events_driven_database.interfaces.documents.chat import EventsDatabaseChatInterface
from databases.events_driven_database.interfaces.documents.user import EventsDatabaseUserInterface

from internal_logger.logger import logger


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
        logger.info('[MessageEventProcessor] attempting to write to database ...')

        EventsDatabaseEventInterface(internal_event=self.internal_event).process()
        EventsDatabaseChatInterface(internal_event=self.internal_event).process()
        EventsDatabaseUserInterface(internal_event=self.internal_event).process()
