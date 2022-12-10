from typing import List, Optional
from pydantic import BaseModel, Field, root_validator, validator

from interfaces.models.validation.location_type import LocationType
from interfaces.models.validation.question_type import QuestionType


class Question(BaseModel):
    """ Question data model, which is used within Questions data model. """

    location_type: LocationType
    question_type: QuestionType

    question: Optional[str]
    question_path: Optional[str]
    index_number: int = Field(gt=0, lt=10)
    answer: str
    attempts_to_fail: int = Field(gt=0, lt=5)

    @root_validator()
    def should_be_either_question_or_path(cls, values):
        """ Validator, which checks whether question and question_path are correctly provided. """

        question = values.get('question')
        question_path = values.get('question_path')

        if question is not None and question_path is not None:
            raise ValueError(' Only one of `question` or `question_path` has to be provided. ')

        elif isinstance(question, str) and question_path is None:
            return values

        elif isinstance(question_path, str) and question is None:
            return values

    @validator('question')
    def set_question_none_type_if_none(cls, value):
        """ Method, which cast str to None type if None was passed. """
        return None if value == 'None' else value

    @validator('question_path')
    def set_question_path_none_type_if_none(cls, value):
        """ Method, which cast str to None type if None was passed. """
        return None if value == 'None' else value


class Questions(BaseModel):
    """ Questions data model, which is supposed to be used in ConversationHandler. """
    questions: List[Question]
