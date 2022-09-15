from typing import Dict
from dataclasses import dataclass, field

from telegram.ext import CommandHandler

from interfaces.telegram_event_handlers.conversation_update.states.builder import StatesBuilder

from interfaces.telegram_event_handlers.conversation_update.commands.start_validation import StartCommandBuilder
from interfaces.telegram_event_handlers.conversation_update.commands.cancel_validation import CancelCommandBuilder

from interfaces.telegram_event_handlers.conversation_update.questions.validator.validator import QuestionsValidator
from interfaces.telegram_event_handlers.conversation_update.questions.preprocessor.preprocessor import QuestionsPreprocessor


@dataclass
class Constructor:
    """ Main Interface to dynamically build ConversationHandler
    based on questions, defined in configurations file. """

    entrypoints: CommandHandler = field(init=False)
    states: Dict = field(init=False)
    fallbacks: CommandHandler = field(default_factory=lambda: CancelCommandBuilder().handler)

    def process(self):
        # validate questions
        questions = QuestionsValidator().questions

        # form questions for states builder
        preprocessed_questions = QuestionsPreprocessor(questions=questions).processed_questions

        for question in preprocessed_questions:

            # if StartCommand question
            if question['question_index'] == 1:
                _entrypoints = StartCommandBuilder(question=question).handler
                self.entrypoints = _entrypoints

            else:
                pass

        return self


cns = Constructor().process()
