from enum import Enum

from telegram.ext import ConversationHandler


class ConversationStates(Enum):
    """ Numeric mapping for conversation states. """

    SECOND_QUESTION_STATE = 2
    THIRD_QUESTION_STATE = 3
    FOURTH_QUESTION_STATE = 4
    GOODBYE_STATE = 5
    FINISH_CONVERSATION_STATE = ConversationHandler.END
