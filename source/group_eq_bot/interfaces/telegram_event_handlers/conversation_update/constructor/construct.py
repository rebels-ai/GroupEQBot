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
    states: Dict = field(default_factory=lambda: {})
    fallbacks: CommandHandler = field(default_factory=lambda: CancelCommandBuilder().handler)

    def __post_init__(self):
        # validate questions
        questions = QuestionsValidator().questions

        # form questions for states builder
        preprocessed_questions = QuestionsPreprocessor(questions=questions).processed_questions

        for question in preprocessed_questions:
            right_answer = question.get('meta').answer

            # if StartCommand question
            if question['question_index'] == 1:
                _entrypoints = StartCommandBuilder(question=question).handler
                self.entrypoints = _entrypoints

            else:
                state = StatesBuilder(question=question).state
                self.states.update(state)

        return self


cns = Constructor()
