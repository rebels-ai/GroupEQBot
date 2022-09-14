from pydantic import BaseModel

from interfaces.models.validation.location_type import LocationType
from interfaces.models.validation.question_type import QuestionType


class Model(BaseModel):
    location_type: LocationType
    question_type: QuestionType
    index_number: int
    question: str
    question_path: str
    answer: str
    attempts_to_fail: int
