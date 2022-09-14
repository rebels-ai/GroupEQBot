from dataclasses import dataclass, field

from interfaces.models.validation.question_type import QuestionType
from interfaces.models.validation.questions import Question
from drivers.local.reader import Reader

from telegram import Update as TelegramEvent
from telegram.ext import CommandHandler, ContextTypes


@dataclass
class StartCommandBuilder:
    """ Interface for `start_validation` command of ConversationHandler. """
    CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

    question: Question = field(init=True)
    handler: CommandHandler = field(init=False)

    command: str = 'start_validation'

    def __post_init__(self):
        self.handler = CommandHandler(command=self.command,
                                      callback=self.callback_function)

    async def callback_function(self, event: TelegramEvent, context: CONTEXT_DEFAULT_TYPE) -> int:
        """ Method, which will be called as a callback for `start_validation` command. """

        next_question_index = self.question.index_number + 1

        # if audio question
        if self.question.question_type == QuestionType.audio:
            audio_object = Reader(input_path=self.question.question_path).read()
            await event.message.reply_voice(voice=audio_object)

        # if text question
        elif self.question.question_type == QuestionType.text:

            # if text question declared in configurations file
            if self.question.question is not None:
                await event.message.reply_text(text=self.question.question)

            # if text question saved in assets
            else:
                text_object = Reader(input_path=self.question.question_path).read()
                await event.message.reply_text(text=text_object)

        return next_question_index
