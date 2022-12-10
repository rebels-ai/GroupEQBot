from typing import Dict
from dataclasses import dataclass, field

from telegram import Update as TelegramEvent
from telegram.ext import CallbackQueryHandler, ContextTypes, ConversationHandler

from interfaces.models.internal_event.chat_type import ChatType
from interfaces.models.validation.question_type import QuestionType
from interfaces.telegram_event_handlers.conversation_update.button.helper import StartButtonHelper

from utilities.configurations_constructor.constructor import Constructor


@dataclass
class StartButtonBuilder:
    """ Interface for button entrypoint of ConversationHandler. """

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

        #  Edit previous message to remove buttons
        await event.callback_query.edit_message_text(text=self.configurator.configurations.bot.validation.validation_started_message)

        str_chat_id = event.callback_query.data

        StartButtonHelper(event=event, context=context).write_event_to_database(chat_id=str_chat_id)

        if event.callback_query.message.chat.type == ChatType.private.value:

            if await StartButtonHelper(event=event, context=context).chat_owner(chat_id=str_chat_id):

                await event.callback_query.message.reply_text(text=self.configurator.configurations.bot.validation.stop_validation_for_owner)
                return ConversationHandler.END

            StartButtonHelper(event=event, context=context).write_time_validation_started(chat_id=str_chat_id)
            context.chat_data['chat_id'] = -int(str_chat_id)  # Save chat_id for later usage in conversation

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
