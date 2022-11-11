from dataclasses import dataclass, field

from telegram.ext import ContextTypes

from utilities.internal_logger.logger import logger
from utilities.configurations_constructor.constructor import Constructor

from interfaces.models.internal_event.event import ExpectedInternalEvent
from storage.schemas.bot_metadata.schema import Builder


@dataclass
class BotEventProcessor:
    """ Main Interface to process Bot Updates.
    
    Notes:
        Interface is suppsoed to be executed JUST and only in the use case, 
        when bot was added to the telegram group
    """

    internal_event: ExpectedInternalEvent
    context: ContextTypes.DEFAULT_TYPE
    configurator: Constructor = field(default_factory=lambda: Constructor())

    async def process(self):
        logger.info('[BotEventProcessor] is called ...')
        logger.info('[BotEventProcessor] attempting to write to storage ...')

        document = Builder(object=self.internal_event).build()
        document.schema.save(index=document.index_name)

        return