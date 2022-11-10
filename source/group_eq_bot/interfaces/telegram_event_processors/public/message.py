from dataclasses import dataclass

from telegram.ext import ContextTypes
from interfaces.models.internal_event.event import ExpectedInternalEvent

from utilities.internal_logger.logger import logger


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
