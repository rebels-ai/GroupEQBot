from typing import Dict
from dataclasses import dataclass, field

from telegram.ext import CommandHandler

from interfaces.telegram_event_handlers.conversation_update.states.builder import StatesBuilder
from interfaces.telegram_event_handlers.conversation_update.commands.start_validation import StartCommandBuilder
from interfaces.telegram_event_handlers.conversation_update.questions.validator.validator import QuestionsValidator
from interfaces.telegram_event_handlers.conversation_update.questions.preprocessor.preprocessor import QuestionsPreprocessor


@dataclass
class Constructor:
    """ Main Interface to dynamically build ConversationHandler
    based on questions, defined in configurations file. """

    entrypoint: CommandHandler = field(init=False)
    states: Dict = field(init=False)
    fallbacks: CommandHandler = field(init=False)

    def process(self):
        # validate questions
        questions = QuestionsValidator().questions

        # form questions for states builder
        classified_questions = QuestionsPreprocessor(questions=questions)

        # form entrypoint
        self.entrypoint = StartCommandBuilder(question=classified_questions.question_for_start_command).handler

        # form states
        self.states = StatesBuilder(text_questions=classified_questions.text_questions,
                                    audio_questions=classified_questions.audio_questions).states

        return self


cns = Constructor().process()