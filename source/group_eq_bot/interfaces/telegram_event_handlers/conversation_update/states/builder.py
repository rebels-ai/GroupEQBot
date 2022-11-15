from typing import Dict, Optional

from dataclasses import dataclass, field
from telegram import Update as TelegramEvent
from telegram.ext import MessageHandler, ContextTypes, filters, ConversationHandler

from interfaces.models.validation.question_type import QuestionType
from interfaces.telegram_event_handlers.conversation_update.states.helpers import StatesHelpers
from utilities.configurations_constructor.constructor import Constructor


@dataclass
class StatesBuilder:
    """ Interface, which builds states, based on input questions. """

    CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

    question: Optional[Dict] = None
    final_question: bool = False

    default_message_handler: MessageHandler = field(default_factory=lambda: MessageHandler)
    default_filters: filters = (filters.TEXT & ~filters.COMMAND)

    state: Dict = field(init=False)
    question_index: int = field(init=False)
    configurator: Constructor = field(default_factory=lambda: Constructor())

    def set_question_index(self) -> int:
        if not self.final_question:
            return self.question['question_index']
        else:
            return StatesHelpers.get_questionnaire_size() + 1

    def __post_init__(self):
        self.question_index = self.set_question_index()
        self.state = {self.question_index: [self.default_message_handler(self.default_filters, self.callable_function)]}

    async def callable_function(self, event: TelegramEvent, context: CONTEXT_DEFAULT_TYPE) -> int:
        """ Method, which will be called as a callback for each message within the conversation. """

        next_question_index = self.question_index + 1

        await StatesHelpers(event=event,
                            context=context,
                            question=self.question).validate_and_save_to_event_database()

        if StatesHelpers(event=event,
                         context=context,
                         question=self.question).answer_is_correct():

            if self.final_question:
                await event.message.reply_text(text=self.configurator.configurations.bot.validation.validation_passed_message)
                await StatesHelpers(event=event,
                                    context=context,
                                    question=self.question).disable_restrictions_for_validated_member()
                StatesHelpers(event=event,
                              context=context,
                              question=self.question).write_time_validation_finished()
                StatesHelpers(event=event,
                              context=context,
                              question=self.question).mark_validation_passed()
                return ConversationHandler.END

            else:
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

        else:
            mistakes_number = StatesHelpers(event=event,
                                            context=context,
                                            question=self.question).increment_mistakes_number(question_identifier=self.question_index)
            # attempts_limit = self.question.get('meta').attempts_to_fail
            attempts_limit = StatesHelpers(event=event,
                                           context=context,
                                           question=self.question).get_attempts_number()

            if mistakes_number < attempts_limit:
                await StatesHelpers(event=event, 
                                    context=context, 
                                    question=self.question).notify_about_remaining_attempts(mistakes_number=mistakes_number)
                return  # return will keep the user on the same state

            else:
                await StatesHelpers(event=event, 
                                    context=context, 
                                    question=self.question).notify_about_failed_validation()
                await StatesHelpers(event=event, 
                                    context=context, 
                                    question=self.question).ban_member_who_failed_validation()
                return ConversationHandler.END
