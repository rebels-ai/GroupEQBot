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

    entrypoints: CommandHandler = field(init=False)  # not initialising here, instead traversing the questions
    states: Dict = field(default_factory=lambda: {})
    fallbacks: CommandHandler = field(default_factory=lambda: CancelCommandBuilder().handler)

    def __post_init__(self):
        questions = QuestionsValidator().questions  # validate questions
        preprocessed_questions = QuestionsPreprocessor(questions=questions).processed_questions  # form questions for states builder

        for question in preprocessed_questions:
            if question['question_index'] == 1:  # if StartCommand (1st question) question
                _entrypoints = StartCommandBuilder(question=question).handler
                self.entrypoints = _entrypoints

            else:
                state = StatesBuilder(question=question).state
                self.states.update(state)

        final_state = StatesBuilder(final_question=True).state
        self.states.update(final_state)

        return self
