from typing import List, Dict

from dataclasses import dataclass, field
from telegram.ext import MessageHandler

from interfaces.models.validation.questions import Question


@dataclass
class StatesBuilder:
    """ Interface, which builds states,
    based on input questions. """

    audio_questions: List[Question] = field(init=True)
    text_questions: List[Question] = field(init=True)

    message_handler: MessageHandler = field(default_factory=lambda: MessageHandler())
    states: Dict = field(init=False)

"""
ConversationStates.SECOND_QUESTION_STATE.value: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                                                Validator().invoke_second_question)]
"""
