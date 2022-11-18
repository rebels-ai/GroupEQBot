from dataclasses import dataclass
import shortuuid
from datetime import datetime

from telegram import Update as TelegramEvent
from telegram.ext import ContextTypes
from elasticsearch_dsl import Q

from storage.schemas.bot_events.schema import Builder, BotEvent, UserEvent, Event, Message
from storage.query.query import update_query, find_query
from utilities.internal_logger.logger import logger


@dataclass
class StartHelper:
    """ Helper methods for StartCommandHandler """

    CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

    event: TelegramEvent
    context: CONTEXT_DEFAULT_TYPE

    async def chat_owner(self, chat_id: str) -> bool:
        """ Method, which checks whether message author is a chat owner. """

        member = await self.context.bot.get_chat_member(
            chat_id=-int(chat_id),
            user_id=self.event.effective_user.id
            )

        return True if member.status == 'creator' else False

    def write_event_to_database(self, chat_id: str):
        logger.info('[BotEventProcessor] attempting to write to storage ...')

        chat_query = Q('match', chat_id=chat_id)
        user_query = Q('bool', must=[chat_query, Q('match', chat_id__user_id=self.event.effective_user.id)])

        shortuuid.set_alphabet('0123456789')
        event_id = int(shortuuid.random(length=16))

        message = Message(event_time=datetime.now(), 
                          content='start button clicked', raw_event=self.event)
        user_event = UserEvent(event_id=event_id, message=message)
        event = Event(user_id=self.event.effective_user.id, user_event=user_event)
        document = BotEvent(chat_id=int(chat_id), event=event)
        index_name = f'{document.Index.name}-bot-events'

        index = document._get_index()
        chat_document = find_query(query=chat_query, index_name=index_name, doc_type=BotEvent)
        user_document = find_query(query=user_query, index_name=index_name, doc_type=BotEvent)

        if index is None or len(chat_document) == 0:
            document.save(index=index_name)
        elif len(user_document) == 0:

            source = "ctx._source.event = params.event"
            params = {"event": document.event}

            update_query(query=chat_query, index_name=index_name, doc_type=BotEvent, source=source, params=params)
        else:

            source = "ctx._source.event.user_event.add(params.user_event)"
            params = {"user_event": document.user_event}

            update_query(query=user_query, index_name=index_name, doc_type=BotEvent, source=source, params=params)
