from typing import Dict
from dataclasses import dataclass, field

from telegram import Update as TelegramEvent
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler

from interfaces.models.validation.question_type import QuestionType
from interfaces.telegram_event_handlers.conversation_update.commands.helper import StartCommandHelper
from utilities.configurations_constructor.constructor import Constructor
from utilities.internal_logger.logger import logger

@dataclass
class StartCommandBuilder:
    """ Interface for `start_validation` command of ConversationHandler. """

    CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

    question: Dict = field(init=True)
    command: str = 'start_validation'

    handler: CommandHandler = field(init=False)

    configurator: Constructor = field(default_factory=lambda: Constructor())

    def __post_init__(self):
        self.handler = [CommandHandler(command=self.command,
                                      callback=self.callback_function)]

    async def callback_function(self, event: TelegramEvent, context: CONTEXT_DEFAULT_TYPE) -> int:
        """ Method, which will be called as a callback for `start_validation` command. """

        if await StartCommandHelper(event=event, context=context).check_if_chat_owner():
            logger.info(f'User, who talks with bot: {event.message.from_user.full_name}')

            await event.message.reply_text(text=self.configurator.configurations.bot.validation.stop_validation_for_owner)
            return ConversationHandler.END

        next_question_index = self.question.get('question_index') + 1
        question_type = self.question.get('meta').question_type

        # if audio question
        if question_type == QuestionType.audio:
            await event.message.reply_voice(voice=self.question.get('question_object'))

        # if text question
        elif question_type == QuestionType.text:

            # if text question declared in configurations file
            if self.question.get('meta').question is not None:
                await event.message.reply_text(text=self.question.get('question_object'))

            # if text question saved in assets
            else:
                await event.message.reply_text(text=self.question.get('question_object'))

        return next_question_index
