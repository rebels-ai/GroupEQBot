from typing import List

from dataclasses import dataclass, field
from interfaces.models.validation.question_type import QuestionType

from interfaces.models.validation.questions import Question


@dataclass
class QuestionsPreprocessor:
    """ Interface, to process and classify validated questions accordingly.

    Usage:
        QuestionsPreprocessor(questions=<validated_questions>)
    """

    questions: List = field(init=True)

    audio_questions: List = field(default_factory=lambda: [])
    text_questions: List = field(default_factory=lambda: [])

    ordered_audio_questions: List = field(default_factory=lambda: [])
    ordered_text_questions: List = field(default_factory=lambda: [])
    question_for_start_command: Question = field(init=False)

    def __post_init__(self):
        self.classify_questions()
        self.order_text_questions()
        self.order_audio_questions()
        self.set_question_for_start_command()

    def classify_questions(self):
        """ Method, which based on QuestionType classifies question. """

        for question in self.questions:
            if question.question_type == QuestionType.audio:
                self.audio_questions.append(question)

            elif question.question_type == QuestionType.text:
                self.text_questions.append(question)

    def order_text_questions(self):
        """ Method, which orders (ascending order) text questions.
        Notes:
            it is done for the sake of building conversation in correct order.
        """

        # if no questions were declared in configurations file
        if len(self.text_questions) <= 0:
            return

        # declaring storage with index_number as the key
        _storage = {}
        for entry in self.text_questions:
            _storage[entry.index_number] = entry

        # sort by ascending order storage and add question accordingly
        for key in sorted(_storage.keys()):
            self.ordered_text_questions.append(_storage[key])

    def order_audio_questions(self):
        """ Method, which orders (ascending order) audio questions.
        Notes:
            it is done for the sake of building conversation in correct order.
        """

        # if no questions were declared in configurations file
        if len(self.audio_questions) <= 0:
            return

        # declaring storage with index_number as the key
        _storage = {}
        for entry in self.audio_questions:
            _storage[entry.index_number] = entry

        # sort by ascending order storage and add question accordingly
        for key in sorted(_storage.keys ()):
            self.ordered_audio_questions.append(_storage[key])

    def set_question_for_start_command(self):
        """ Method, which find by index_number question to be set for start conversation. """

        # audio
        if len(self.ordered_audio_questions) > 0 and self.ordered_audio_questions[0].index_number == 1:
            self.question_for_start_command = self.ordered_audio_questions[0]
            # make sure we do not hold question in ordered list,
            # which is already in use for starting question
            self.ordered_audio_questions.pop(0)

        # text
        elif len(self.ordered_text_questions) > 0 and self.ordered_text_questions[0].index_number == 1:
            self.question_for_start_command = self.ordered_audio_questions[0]
            # make sure we do not hold question in ordered list,
            # which is already in use for starting question
            self.ordered_text_questions.pop(0)

        else:
            raise ValueError('NotFound question with index_name == 1.'
                             'Correct configurations file.')