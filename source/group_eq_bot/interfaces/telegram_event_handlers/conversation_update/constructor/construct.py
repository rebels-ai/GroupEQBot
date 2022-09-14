from typing import Any

from dataclasses import dataclass, field
from pydantic import ValidationError

from utilities.configurations_constructor.constructor import Constructor as ConfigurationsConstructor

from interfaces.models.validation.questions import Question, Questions

"""
1. Read questions attribute from configurations
2. Validate whether question alignes with Question Data Model

3. Based on QuestionType we need to build question(S) state(S)
4. Pass that question state to ConversationHandler
"""


@dataclass
class QuestionsValidator:
    """ Interface to get and validate questions from configurations file.

    Usage:
        QuestionsValidator().questions
    """

    configurator: ConfigurationsConstructor = field(default_factory=lambda: ConfigurationsConstructor())
    questions: Any = field(init=False)

    def __post_init__(self):
        self.get_questions_from_configurations()
        self.validate_questions()

    def get_questions_from_configurations(self):
        """ Method, which parses list of questions, declared in configurations file. """
        self.questions = self.configurator.configurations.bot.validation.questions

    def validate_questions(self):
        """ Method, which validates questions from configurations file against Question data model. """

        try:
            _questions_to_validate = [Question(**entry) for entry in self.questions]
            self.questions = Questions(questions=_questions_to_validate).questions
        except ValidationError as error:
            raise error

