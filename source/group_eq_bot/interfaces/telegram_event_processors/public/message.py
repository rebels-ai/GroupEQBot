from dataclasses import dataclass

from telegram.ext import ContextTypes

from interfaces.models.internal_event.event import ExpectedInternalEvent
from utilities.internal_logger.logger import logger
from storage.schemas.group_events.schema import Builder


@dataclass
class MessageEventProcessor:
    """ Main Interface to process Messages Updates. """

    internal_event: ExpectedInternalEvent
    context: ContextTypes.DEFAULT_TYPE

    async def process(self) -> None:
        """
        Entrypoint to process Public Message (ExpectedInternalEvent)
        event and write it to EventDrivenDatabase.
        """

        logger.info('[MessageEventProcessor] is called ...')
        self._write_event_to_datase()

    def _write_event_to_datase(self) -> None:
        """ Function, which generates Event document from ExpectedInternalEvent and saves it to database """

        logger.info('[MessageEventProcessor] attempting to write event document to storage ...')

        document = Builder(object=self.internal_event).build()
        document.schema.save(index=document.index_name)
