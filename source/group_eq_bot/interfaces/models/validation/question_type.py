from enum import Enum


class QuestionType(Enum):
    """ Data model for types of the question files, used in ConversationHandler. """
    audio = 'audio'
    text = 'text'
