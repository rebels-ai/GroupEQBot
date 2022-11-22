from dataclasses import dataclass, field

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from elasticsearch_dsl import Q

from utilities.internal_logger.logger import logger
from utilities.configurations_constructor.constructor import Constructor

from storage.schemas.group_users.schema import Builder, GroupUser
from storage.schemas.chats_mappings.schema import ChatsMapping
from storage.query.query import update_query, find_query, search_in_existing_index

from interfaces.models.internal_event.member_status import MemberStatus
from interfaces.models.internal_event.event import ExpectedInternalEvent


@dataclass
class BotEventProcessor:
    """ Main Interface to process bot updates.

    Constraint:
        Interface is supposed to be executed JUST and only in the use case,
        when bot was added to the telegram group
    """

    internal_event: ExpectedInternalEvent
    context: ContextTypes.DEFAULT_TYPE
    configurator: Constructor = field(default_factory=lambda: Constructor())

    async def process(self):
        """ Entrypoint for the BotProcessor, which based on the bot StatusChange event, invoke appropriate logic. """

        logger.info('[BotEventProcessor] is called ...')

        # User started conversation with bot
        if self.internal_event.old_status == MemberStatus.left.value \
            or self.internal_event.old_status == MemberStatus.banned.value \
                and self.internal_event.new_status == MemberStatus.member.value:

            self._write_event_to_datase()
            await self.context.bot.send_message(chat_id=self.internal_event.event.my_chat_member.from_user.id, 
                                                text=self.configurator.configurations.bot.validation.instruction)

        # User stopped the bot
        elif self.internal_event.old_status == MemberStatus.member.value \
            and self.internal_event.new_status == MemberStatus.left.value \
                or self.internal_event.new_status == MemberStatus.banned.value:

            self._write_event_to_datase()

        else:
            logger.info(f'[UNEXPECTED EVENT] bot was {self.internal_event.old_status}, became {self.internal_event.new_status}')

        return

    def _write_event_to_datase(self):
        pass
