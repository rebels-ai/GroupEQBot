from dataclasses import dataclass, field
from typing import Dict, Optional

from telegram import ChatPermissions
from telegram import Update as TelegramEvent
from telegram.ext import ContextTypes

from interfaces.telegram_event_validator.validator import EventValidator
from interfaces.telegram_event_processors.public.message import MessageEventProcessor
from utilities.configurations_constructor.constructor import Constructor
from utilities.internal_logger.logger import logger


@dataclass
class StatesHelpers:
    """ Helper methods for StatesBuilder """

    CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

    event: TelegramEvent
    context: CONTEXT_DEFAULT_TYPE

    question: Optional[Dict] = None
    configurator: Constructor = field(default_factory=lambda: Constructor())

    def retrieve_member_answer(self) -> str:
        """ Helper function, which retrieves member reply from TelegramEvent. """

        try:
            member_answer = self.event.message.text
            return member_answer

        except KeyError as error:
            raise f'Got unexpected event data model. Can not get "event.message.text" key. \n ' \
                  f'{error}'

    def answer_is_correct(self) -> bool:
        """ Helper function which validates member's reply on any question. """

        member_answer = self.retrieve_member_answer()
        right_answer = self.get_right_answer()
        return True if member_answer == right_answer else False

    def increment_mistakes_number(self, question_identifier: str) -> int:
        """ Function, which increment amount of mistakes per validation question.
        Note:
             per each question we intend to have dedicated key:value counter pair.
        """

        self.context.user_data[question_identifier] = self.context.user_data.get(question_identifier, 0) + 1
        return self.context.user_data[question_identifier]

    async def notify_about_remaining_attempts(self, mistakes_number: int) -> None:
        """ Function, which notifies the member's reply failure. """

        attempts_limit = int(self.get_attempts_number())
        notification = self.configurator.configurations.bot.validation.remaining_attemps_message
        text = f'{notification} {attempts_limit - mistakes_number}'
        await self.event.message.reply_text(text=text)

        return

    async def notify_about_failed_validation(self) -> None:
        """ Function, which notifies member's verification failure. """

        notification = self.configurator.configurations.bot.validation.validation_failed_message
        await self.event.message.reply_text(text=notification)
        return

    def get_chat_id_for_validation(self) -> Optional[int]:
        """ Function, which finds chat id which member recently joined,
        and passing the validation process. """

        return self.context.user_data.get('chat_id', 0)

    async def disable_restrictions_for_validated_member(self):
        """ Function, which changes status from restricted on member,
        disabling restrictions for user, who passed the validation.  """

        chat_id = self.get_chat_id_for_validation()
        await self.context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=self.event.message.from_user.id,

            permissions=ChatPermissions(
                can_send_messages=True,  # to be able to reply ConversationHandler messages
                can_send_other_messages=True,
                can_invite_users=True,
                can_send_polls=True,
                can_send_media_messages=True,
                can_change_info=True,
                can_pin_messages=True,
                can_add_web_page_previews=True
            )
        )
        self.context.user_data.clear()

    async def ban_member_who_failed_validation(self):
        """ Function, which changes status from restricted on restricted,
        banning user, who failed validation process. """

        chat_id = self.get_chat_id_for_validation()
        await self.context.bot.ban_chat_member(chat_id=chat_id,
                                               user_id=self.event.message.from_user.id)
        self.context.user_data.clear()

    async def validate_and_save_to_event_database(self):
        """ Function, responsible for validating incoming TelegramEvent
            and saving it to event database. """

        logger.info('[NEW MEMBER VALIDATION] New Event Registered.')
        event = EventValidator(external_event=self.event).validated_internal_event
        logger.info('[NEW MEMBER VALIDATION] New Event Validated and Casted in ExpectedInternalEvent.')

        await MessageEventProcessor(internal_event=event,
                                    context=self.context).process()

    @staticmethod
    def get_questionnaire_size() -> int:
        """ Function, which gets the amount of questions in validation process. """

        return len(Constructor().configurations.bot.validation.questions)

    def get_right_answer(self) -> str:
        """ Function, which gets the right answer defined in configurations. """

        return self.get_previous_question().answer

    def get_attempts_number(self) -> int:
        """ Function, which gets the attempts number for this question. """

        return self.get_previous_question().attempts_to_fail

    def get_previous_question(self) -> Dict:
        """ Function, which gets previous question metadata. """

        question_index = self.question.get('question_index') - 1 if self.question is not None else self.get_questionnaire_size()
        questions_list = sorted(self.configurator.configurations.bot.validation.questions, key=lambda d: d['index_number'])
        previous_question = questions_list[question_index - 1]  # questions indexes starts from 1, list indexes from 0

        return previous_question
