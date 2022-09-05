from dataclasses import dataclass
from io import BufferedReader
from typing import Union

from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra

from telegram import Update as TelegramEvent
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes

from utilities.internal_logger.logger import logger
from interfaces.models.conversation_handler_states import ConversationStates
from telegram_event_handlers.conversations.validation.helpers import ConversationValidatorHelpers


# Fetch bot configuration with hydra compose api
# https://hydra.cc/docs/advanced/compose_api/
initialize(version_base="1.2", config_path="../../../configurations", job_name="conversation_validation_handler")
configurations = compose(config_name="configuration")
GlobalHydra.instance().clear()

LIMIT_OF_ATTEMPTS_TO_FAIL_PER_QUESTION: int = int(configurations.validation.limit_of_attempts_to_fail_per_question)
MATHEMATICAL_ANSWER: str = configurations.validation.mathematical_answer


@dataclass
class Validator:
    CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

    @staticmethod
    async def invoke_first_question(event: TelegramEvent, context: CONTEXT_DEFAULT_TYPE) -> Union[int, None]:
        """ Function, which holds the logic for 1-st ConversationValidationHandler state. """

        if await ConversationValidatorHelpers(event=event, context=context).check_if_chat_owner():
            logger.info(f'User, who talks with bot: {event.message.from_user.full_name}')

            await event.message.reply_text(text='You are the owner! No need to validate yourself ^_^ ')
            return ConversationStates.FINISH_CONVERSATION_STATE.value

        else:
            logger.info(f'User, who talks with bot: {event.message.from_user.full_name}')

            question = ConversationValidatorHelpers.load_question('first')
            await ConversationValidatorHelpers.reply(event=event, question=question)
            return ConversationStates.SECOND_QUESTION_STATE.value

    @staticmethod
    async def invoke_second_question(event: TelegramEvent, context: CONTEXT_DEFAULT_TYPE) -> Union[int, None]:
        """ Function, which holds the logic for 2-nd ConversationValidationHandler state. """

        logger.info(f'User, who talks with bot: {event.message.from_user.full_name}')
        reply = ConversationValidatorHelpers(event=event, context=context).retrieve_answer_text_from_event()
        validated_reply = ConversationValidatorHelpers(event=event, context=context).validate_reply(reply=reply)

        if validated_reply is True:

            question = ConversationValidatorHelpers.load_question('second')
            await ConversationValidatorHelpers.reply(event=event, question=question)
            return ConversationStates.THIRD_QUESTION_STATE.value

        else:
            failed_attempts = ConversationValidatorHelpers(event=event, context=context).\
                increment_failed_attempts(question_identifier=configurations.validation.questions_paths.first)

            if LIMIT_OF_ATTEMPTS_TO_FAIL_PER_QUESTION != failed_attempts:
                await ConversationValidatorHelpers(event=event, context=context).\
                    notify_about_remaining_attempts(failure_attempts=failed_attempts)
                return  # return will keep the user on the same state

            else:
                await ConversationValidatorHelpers(event=event, context=context).notify_about_failed_validation()
                await ConversationValidatorHelpers(event=event, context=context).ban_member_who_failed_validation()
                return ConversationStates.FINISH_CONVERSATION_STATE.value

    @staticmethod
    async def invoke_third_question(event: TelegramEvent, context: CONTEXT_DEFAULT_TYPE) -> Union[int, None]:
        """ Function, which holds the logic for 3-rd ConversationValidationHandler state. """

        logger.info(f'User, who talks with bot: {event.message.from_user.full_name}')
        reply = ConversationValidatorHelpers(event=event, context=context).retrieve_answer_text_from_event()
        validated_reply = ConversationValidatorHelpers(event=event, context=context).validate_reply(reply=reply)

        if validated_reply is True:
            question = ConversationValidatorHelpers.load_question('third')
            await ConversationValidatorHelpers.reply(event=event, question=question)
            return ConversationStates.FOURTH_QUESTION_STATE.value

        else:
            failed_attempts = ConversationValidatorHelpers(event=event, context=context).\
                increment_failed_attempts(question_identifier=configurations.validation.questions_paths.second)

            if LIMIT_OF_ATTEMPTS_TO_FAIL_PER_QUESTION != failed_attempts:
                await ConversationValidatorHelpers(event=event, context=context).\
                    notify_about_remaining_attempts(failure_attempts=failed_attempts)
                return  # return will keep the user on the same state

            else:
                await ConversationValidatorHelpers(event=event, context=context).notify_about_failed_validation()
                await ConversationValidatorHelpers(event=event, context=context).ban_member_who_failed_validation()
                return ConversationStates.FINISH_CONVERSATION_STATE.value

    @staticmethod
    async def invoke_fourth_question(event: TelegramEvent, context: CONTEXT_DEFAULT_TYPE) -> Union[int, None]:
        """ Function, which holds the logic for 4-th ConversationValidationHandler state. """

        logger.info(f'User, who talks with bot: {event.message.from_user.full_name}')
        reply = ConversationValidatorHelpers(event=event, context=context).retrieve_answer_text_from_event()
        validated_reply = ConversationValidatorHelpers(event=event, context=context).validate_reply(reply=reply)

        if validated_reply is True:
            question = ConversationValidatorHelpers.load_question('fourth')
            await ConversationValidatorHelpers.reply(event=event, question=question)
            return ConversationStates.GOODBYE_STATE.value

        else:
            failed_attempts = ConversationValidatorHelpers(event=event, context=context).\
                increment_failed_attempts(question_identifier=configurations.validation.questions_paths.third)

            if LIMIT_OF_ATTEMPTS_TO_FAIL_PER_QUESTION != failed_attempts:
                await ConversationValidatorHelpers(event=event, context=context).\
                    notify_about_remaining_attempts(failure_attempts=failed_attempts)
                return  # return will keep the user on the same state

            else:
                await ConversationValidatorHelpers(event=event, context=context).notify_about_failed_validation()
                await ConversationValidatorHelpers(event=event, context=context).ban_member_who_failed_validation()
                return ConversationStates.FINISH_CONVERSATION_STATE.value

    @staticmethod
    async def say_goodbye(event: TelegramEvent, context: CONTEXT_DEFAULT_TYPE) -> Union[int, None]:
        """ Function, which holds the logic for the last ConversationValidationHandler state. """

        logger.info(f'User, who talks with bot: {event.message.from_user.full_name}')
        reply = ConversationValidatorHelpers(event=event, context=context).retrieve_answer_text_from_event()
        validated_reply = ConversationValidatorHelpers(event=event, context=context).\
            validate_reply(reply=reply, mathematical_question=True)

        if validated_reply is True:
            question = ConversationValidatorHelpers.load_question('goodbye')
            await ConversationValidatorHelpers.reply(event=event, question=question)
            await ConversationValidatorHelpers(event=event, context=context).disable_restrictions_for_validated_member()
            return ConversationStates.FINISH_CONVERSATION_STATE.value

        else:
            failed_attempts = ConversationValidatorHelpers(event=event, context=context).\
                increment_failed_attempts(question_identifier=configurations.validation.questions_paths.fourth)

            if LIMIT_OF_ATTEMPTS_TO_FAIL_PER_QUESTION != failed_attempts:
                await ConversationValidatorHelpers(event=event, context=context).\
                    notify_about_remaining_attempts (failure_attempts=failed_attempts)
                return  # return will keep the user on the same state

            else:
                await ConversationValidatorHelpers(event=event, context=context).notify_about_failed_validation()
                await ConversationValidatorHelpers(event=event, context=context).ban_member_who_failed_validation()
                return ConversationStates.FINISH_CONVERSATION_STATE.value

    @staticmethod
    async def cancel_conversation(event: TelegramEvent, context: CONTEXT_DEFAULT_TYPE) -> int:
        """ Function, which holds the logic for the /cancel ConversationValidationHandler state. """

        logger.info(f'User who canceled conversation: {event.message.from_user.full_name}')
        await event.message.reply_text(text=" To try again type '/start' ")

        return ConversationStates.FINISH_CONVERSATION_STATE.value


ConversationValidatorHandler = ConversationHandler(
    entry_points=[CommandHandler('start', callback=Validator().invoke_first_question)],
    states={
        ConversationStates.SECOND_QUESTION_STATE.value: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                                                        Validator().invoke_second_question)],

        ConversationStates.THIRD_QUESTION_STATE.value: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                                                       Validator().invoke_third_question)],

        ConversationStates.FOURTH_QUESTION_STATE.value: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                                                       Validator().invoke_fourth_question)],

        ConversationStates.GOODBYE_STATE.value: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                                                Validator().say_goodbye)]
    },
    fallbacks=[CommandHandler('cancel', callback=Validator().cancel_conversation)]
    )
