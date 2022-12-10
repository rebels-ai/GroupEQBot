from io import BufferedReader
from typing import List, Dict, Union

from dataclasses import dataclass, field

from drivers.local.reader import Reader
from interfaces.models.validation.questions import Question
from interfaces.models.validation.question_type import QuestionType


@dataclass
class QuestionsPreprocessor:
    """ Interface, to process and classify validated questions accordingly.

    Usage:
        QuestionsPreprocessor(questions=<validated_questions>)
    """

    questions: List = field(init=True)
    processed_questions: List[Dict] = field(default_factory=lambda: [])

    def __post_init__(self):
        self.process()

    @staticmethod
    def retrieve_question_index_number(question: Question) -> int:
        """ Method, which retrieves index_number from question. """
        return question.index_number

    @staticmethod
    def read_question_object(question: Question) -> Union[str, BufferedReader]:
        """ Method, which reads question, depending on its location and type. """

        # if audio question
        if question.question_type == QuestionType.audio:
            question_object = Reader(input_path=question.question_path).read()
            return question_object

        # if text question
        elif question.question_type == QuestionType.text:
            # if text question declared in configurations file
            if question.question is not None:
                question_object = question.question
                return question_object

            # if text question saved in assets
            else:
                question_object = Reader(input_path=question.question_path).read()
                return question_object

    def sort_question(self) -> None:
        """ Method, which sorts questions list[dict] by key. """
        self.processed_questions = sorted(self.processed_questions, key=lambda d: list(d.keys()))

    def process(self) -> None:
        """ QuestionsPreprocessor main interface. """

        for question in self.questions:
            question_index = self.retrieve_question_index_number(question)
            question_object = self.read_question_object(question=question)
            self.processed_questions.append(
                {'question_index': question_index,
                 'question_object': question_object,
                 'meta': question}
            )

        self.sort_question()


