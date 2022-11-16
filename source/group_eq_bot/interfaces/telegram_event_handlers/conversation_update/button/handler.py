from typing import Dict
from dataclasses import dataclass, field
from datetime import datetime

from telegram import Update as TelegramEvent
from telegram.ext import CallbackQueryHandler, ContextTypes, ConversationHandler
from elasticsearch_dsl import Q

from interfaces.models.internal_event.chat_type import ChatType
from interfaces.models.validation.question_type import QuestionType
from interfaces.telegram_event_handlers.conversation_update.button.helper import StartHelper

from utilities.configurations_constructor.constructor import Constructor
from utilities.internal_logger.logger import logger

from storage.schemas.group_users.schema import GroupUser
from storage.query.query import search_in_existing_index, update_query


@dataclass
class StartButtonBuilder:
    """ Interface for button callback entrypoint of ConversationHandler. """

    CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

    question: Dict = field(init=True)

    handler: CallbackQueryHandler = field(init=False)
    configurator: Constructor = field(default_factory=lambda: Constructor())

    def __post_init__(self):
        self.handler = CallbackQueryHandler(callback=self.callback_function, 
                                            pattern=str)

    async def callback_function(self, event: TelegramEvent, context: CONTEXT_DEFAULT_TYPE) -> int:
        """ Method, which will be called as a callback when button with chat_id was clicked. 
            
            Note:
                ConversationHandler supposed to be used only within private chat (bot:user)
        """

        # ConversationHandler supposed to be used only within private chat (bot:user)
        if event.callback_query.message.chat.type == ChatType.private.value:

            if await StartHelper(event=event, context=context).chat_owner(chat_id=event.callback_query.data):
                logger.info(f'User, who talks with bot: {event.callback_query.from_user.full_name}')

                await event.callback_query.message.reply_text(text=self.configurator.configurations.bot.validation.stop_validation_for_owner)
                return ConversationHandler.END

            query = Q('match', user_id=event.callback_query.from_user.id)
            index_name = f'{GroupUser.Index.name}-group-users-{event.callback_query.data}'
            user_doc = search_in_existing_index(query=query, index_name=index_name, doc_type=GroupUser)

            source = "ctx._source.event.validation.start_time = params.start_time"
            params = {"start_time": datetime.now()}

            update_query(query=query, index_name=index_name, doc_type=GroupUser, source=source, params=params)

            context.chat_data['chat_id'] = -int(event.callback_query.data)
            next_question_index = self.question.get('question_index') + 1
            question_type = self.question.get('meta').question_type

            # if audio question
            if question_type == QuestionType.audio:
                await event.callback_query.message.reply_voice(voice=self.question.get('question_object'))

            # if text question
            elif question_type == QuestionType.text:

                # if text question declared in configurations file
                if self.question.get('meta').question is not None:
                    await event.callback_query.message.reply_text(text=self.question.get('question_object'))

                # if text question saved in assets
                else:
                    await event.callback_query.message.reply_text(text=self.question.get('question_object'))

            return next_question_index
