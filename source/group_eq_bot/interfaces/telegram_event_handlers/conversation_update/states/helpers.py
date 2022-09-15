from dataclasses import dataclass, field
from typing import Dict

from telegram import ChatPermissions
from telegram import Update as TelegramEvent
from telegram.ext import ContextTypes

from utilities.internal_logger.logger import logger
from interfaces.telegram_event_validator.validator import EventValidator
from interfaces.telegram_event_processors.public.message import MessageEventProcessor


@dataclass
class StatesHelpers:
    """ Helper methods for StatesBuilder """
    CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

    event: TelegramEvent
    context: CONTEXT_DEFAULT_TYPE

    right_answer: str
    question: Dict = field(init=True)

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
        right_answer = self.right_answer
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

        attempts_limit = self.question.get('meta').attempts_to_fail
        text = f'''
            I got unexpected answer -_- Please listen to the question one more time! \n
            Left attempts for this question: {attempts_limit - mistakes_number}.
            '''
        await self.event.message.reply_text(text=text)
        return

    async def notify_about_failed_validation(self) -> None:
        """ Function, which notifies member's verification failure. """

        text = f"""
            I got too many unexpected answers and there are no more attempts. \n
            Verification failed and you will not get the access to the group O_O.
            """

        await self.event.message.reply_text(text=text)
        return

    async def disable_restrictions_for_validated_member(self):
        """ Function, which changes status from restricted on member,
        disabling restrictions for user, who passed the validation.  """

        await self.context.bot.restrict_chat_member(
            chat_id=self.event.message.chat.id,
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

    async def ban_member_who_failed_validation(self):
        """ Function, which changes status from restricted on restricted,
        banning user, who failed validation process. """

        await self.context.bot.ban_chat_member(chat_id=self.event.message.chat.id,
                                               user_id=self.event.message.from_user.id)

    async def validate_and_save_to_event_database(self):
        """ Function, responsible for validating incoming TelegramEvent
            and saving it to event database. """

        logger.info('[NEW MEMBER VALIDATION] New Event Registered.')
        event = EventValidator(external_event=self.event).validated_internal_event
        logger.info('[NEW MEMBER VALIDATION] New Event Validated and Casted in ExpectedInternalEvent.')

        await MessageEventProcessor(internal_event=event,
                                    context=self.context).process()
