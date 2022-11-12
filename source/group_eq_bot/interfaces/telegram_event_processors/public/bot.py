from dataclasses import dataclass, field

from telegram.ext import ContextTypes
from elasticsearch_dsl import Q

from utilities.internal_logger.logger import logger
from utilities.configurations_constructor.constructor import Constructor

from storage.schemas.bot_metadata.schema import Builder, BotMetadata
from storage.query.query import update_query, find_query

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

        # Bot was added to the group
        if self.internal_event.old_status == MemberStatus.left.value \
            or self.internal_event.old_status == MemberStatus.banned.value \
                and self.internal_event.new_status == MemberStatus.member.value:

            self._write_event_to_datase()

        # Bot became an admin
        elif self.internal_event.new_status == MemberStatus.administrator.value:

            self._write_event_to_datase()

        # Bot was deleted from the group
        elif self.internal_event.old_status == MemberStatus.member.value \
            or self.internal_event.old_status == MemberStatus.administrator.value \
                and self.internal_event.new_status == MemberStatus.left.value \
                    or self.internal_event.new_status == MemberStatus.banned.value:

            self._write_event_to_datase()

        # Bot was demoted from admins
        elif self.internal_event.old_status == MemberStatus.administrator.value \
            and self.internal_event.new_status == MemberStatus.member.value \
                or self.internal_event.new_status == MemberStatus.restricted.value:

            self._write_event_to_datase()

        else:
            logger.info(f'[UNEXPECTED EVENT] bot was {self.internal_event.old_status}, became {self.internal_event.new_status}')

        return

    def _write_event_to_datase(self):
        logger.info('[BotEventProcessor] attempting to write to storage ...')

        query = Q('match', chat_id=abs(self.internal_event.chat_id))
        document = Builder(object=self.internal_event).build()

        index = document.schema._get_index()
        chat_document = find_query(query=query, index_name=document.index_name, doc_type=BotMetadata)

        if index is None or chat_document is None:

            document.schema.save(index=document.index_name)
        else:

            source = "ctx._source.event.bot_status = params.bot_status"
            params = {"bot_status": self.internal_event.new_status}

            update_query(query=query, index_name=document.index_name, doc_type=BotMetadata, source=source, params=params)

