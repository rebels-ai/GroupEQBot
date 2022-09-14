from dataclasses import dataclass
from telegram.ext import ContextTypes

from interfaces.models.internal_event.event import ExpectedInternalEvent
from utilities.internal_logger.logger import logger


@dataclass
class Processor:

    internal_event: ExpectedInternalEvent
    context: ContextTypes.DEFAULT_TYPE

    def handle(self) -> None:
        logger.info('[PROCESSOR] is called.')
        logger.info('[PROCESSOR] finished.')
        return
