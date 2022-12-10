from dataclasses import dataclass
from datetime import datetime
import shortuuid

from telegram import Update as TelegramEvent
from telegram.ext import ContextTypes
from elasticsearch_dsl import Q

from storage.schemas.bot_events.schema import BotEvent, UserEvent, Event, Message
from storage.schemas.group_users.schema import GroupUser
from storage.query.query import update_query
from storage.connectors.connector import connection
from utilities.internal_logger.logger import logger


@dataclass
class StartButtonHelper:
    """ Helper methods for StartButtonBuilder """

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

    def write_event_to_database(self, chat_id: str) -> None:
        """ Function, which writes event to database when user clicked the button. """

        logger.info('[ConversationHandler] attempting to write event doc to storage ...')

        shortuuid.set_alphabet('0123456789')
        event_id = int(shortuuid.random(length=16))

        message = Message(event_time=datetime.now(), 
                          content='start button clicked', raw_event=self.event.to_dict())
        user_event = UserEvent(event_id=event_id, message=message)
        event = Event(user_id=self.event.effective_user.id, user_event=user_event)
        document = BotEvent(chat_id=int(chat_id), event=event)
        index_name = f'{document.Index.name}-bot-events'

        document.save(index=index_name)

    def write_time_validation_started(self, chat_id: str) -> None:
        """ Function, which writes validation start_time in user document. """

        query = Q('match', user_id=self.event.effective_user.id)
        index_name = f'{GroupUser.Index.name}-group-users-{chat_id}'
        source = "ctx._source.event.validation.end_time = params.end_time"
        params = {"end_time": datetime.now()}

        connection.indices.refresh(index=index_name)
        update_query(query=query, index_name=index_name, doc_type=GroupUser, source=source, params=params)
