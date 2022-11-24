from dataclasses import dataclass, field

from telegram.ext import ContextTypes

from utilities.internal_logger.logger import logger
from utilities.configurations_constructor.constructor import Constructor

from interfaces.models.internal_event.member_status import MemberStatus
from interfaces.models.internal_event.event import ExpectedInternalEvent


@dataclass
class BotEventProcessor:
    """ Main Interface to process bot status updates.

    Constraint:
        Interface is supposed to be executed JUST and only in the use case,
        when bot has been started by user in 1:1 private chat
    """

    internal_event: ExpectedInternalEvent
    context: ContextTypes.DEFAULT_TYPE
    configurator: Constructor = field(default_factory=lambda: Constructor())

    async def process(self) -> None:
        """ Entrypoint for the BotEventProcessor, which based on the bot StatusChange event, invoke appropriate logic. """

        logger.info('[BotEventProcessor] is called ...')

        # User started conversation with bot with command /start
        if self.internal_event.old_status == MemberStatus.left.value \
            or self.internal_event.old_status == MemberStatus.banned.value \
                and self.internal_event.new_status == MemberStatus.member.value:

            await self.context.bot.send_message(chat_id=self.internal_event.event.my_chat_member.from_user.id, 
                                                text=self.configurator.configurations.bot.validation.instruction)

        else:
            logger.info(f'[UNEXPECTED EVENT] bot was {self.internal_event.old_status}, became {self.internal_event.new_status}')

        return
