from typing import List, Dict

from dataclasses import dataclass, field
from telegram.ext import MessageHandler, ContextTypes, filters

from interfaces.models.validation.questions import Question


@dataclass
class StatesBuilder:
    """ Interface, which builds states, based on input questions. """

    CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

    question: Dict = field(init=True)
    default_message_handler: MessageHandler = field(default_factory=lambda: MessageHandler)
    default_filters: filters = filters.TEXT & ~filters.COMMAND

    state: Dict = field(init=False)
    question_index: int = field(init=False)

    def set_next_question_index(self):
        self.question_index = self.question.get('index_number')

    def __post_init__(self):
        self.state = {self.question_index: [self.default_message_handler(self.default_filters),
                                            callable_function]}

    def callable_function(self,event: TelegramEvent, context: CONTEXT_DEFAULT_TYPE) -> int:
        pass
