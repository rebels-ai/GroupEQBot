from dataclasses import dataclass
from io import BufferedReader

from telegram import ChatPermissions
from telegram import Update as TelegramEvent
from telegram.ext import ContextTypes

from utilities.internal_logger.logger import logger
from drivers.local.reader import Reader
from interfaces.telegram_event_validator.validator import EventValidator
from interfaces.telegram_event_processors.public.message import MessageEventProcessor

from utilities.configurations_constructor.constructor import Constructor
CONFIGURATIONS = Constructor().configurations

LIMIT_OF_ATTEMPTS_TO_FAIL_PER_QUESTION: int = int(CONFIGURATIONS.bot.validation.limit_of_attempts_to_fail_per_question)
MATHEMATICAL_ANSWER: str = CONFIGURATIONS.bot.validation.mathematical_answer


@dataclass
class ConversationValidatorHelpers:
    CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

    event: TelegramEvent
    context: CONTEXT_DEFAULT_TYPE

    async def check_if_chat_owner(self) -> bool:
        """ Function, which checks whether message author is a chat owner """
        member = await self.context.bot.get_chat_member(
            chat_id=self.event.effective_chat.id,
            user_id=self.event.effective_user.id
            )
        logger.info(member.status)
        return True if member.status == 'creator' else False

    def retrieve_answer_text_from_event(self) -> str:
        """ Helper function, which retrieves member reply from TelegramEvent. """

        try:
            member_answer = self.event.message.text
            return member_answer

        except KeyError as error:
            raise f'Got unexpected event data model. Can not get "event.message.text" key. \n ' \
                  f'{error}'

    @staticmethod
    def validate_reply(reply: str, mathematical_question: bool = False) -> bool:
        """ Helper function which validates member's reply on any question.

        Notes:
            - telegram does not allow sending (meaning, we do not have to perform these cases):
                 - just space(S) characters
                 - just backspace(S) characters
            - when mathematical_question == True
                - expression asked to count is: 23 + 17 = 40
        """

        if mathematical_question is False:
            joined_reply = ''.join(entity.strip() for entity in reply.split())
            return True if joined_reply.isalpha() is True else False
        else:
            return True if reply == str(MATHEMATICAL_ANSWER) else False

    def increment_failed_attempts(self, question_identifier: str) -> int:
        """ Function, which increment amount of failures per validation question.
        Note:
             per each question we intend to have dedicated key:value counter pair.
        """

        self.context.user_data[question_identifier] = self.context.user_data.get(question_identifier, 0) + 1
        return self.context.user_data[question_identifier]

    async def notify_about_remaining_attempts(self, failure_attempts: int) -> None:
        """ Function, which notifies the member's reply failure. """

        text = f'''
            I got unexpected answer -_- Please listen to the question one more time! \n
            Left attempts for this question: {LIMIT_OF_ATTEMPTS_TO_FAIL_PER_QUESTION - failure_attempts}.
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

    @staticmethod
    async def reply_question(event: TelegramEvent, question_number: str):
        """ Function, which will call reply text or voice depending on question extension."""

        question = Reader(configurations.validation.questions_paths[question_number]).read()

        if isinstance(question, str):
            await event.message.reply_text(text=question)
        elif isinstance(question, BufferedReader):
            await event.message.reply_voice(voice=question)
        else:
            logger.info('File read is neither text nor audio')

    async def validate_and_save_to_event_database(event: TelegramEvent, context: CONTEXT_DEFAULT_TYPE):
        """ Function, responsible for validating incoming TelegramEvent
            and saving it to event database. """
            
        logger.info('[NEW MEMBER VALIDATION] New Event Registered.')
        event = EventValidator(external_event=event).validated_internal_event
        logger.info('[NEW MEMBER VALIDATION] New Event Validated and Casted in ExpectedInternalEvent.')

        await MessageEventProcessor(internal_event=event,
                                    context=context).process()
