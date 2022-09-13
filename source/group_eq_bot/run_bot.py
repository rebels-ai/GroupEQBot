from typing import Union, Any
from telegram.ext import ApplicationBuilder, Application

from interfaces.telegram_event_handlers.member_update.handler import MemberHandler
from interfaces.telegram_event_handlers.message_update.text.handler import TextMessageHandler
from interfaces.telegram_event_handlers.message_update.video.handler import VideoMessageHandler
from interfaces.telegram_event_handlers.message_update.audio.handler import AudioMessageHandler
from interfaces.telegram_event_handlers.message_update.document.handler import DocumentMessageHandler
from interfaces.telegram_event_handlers.conversation_update.handler import ConversationValidatorHandler

from utilities.internal_logger.logger import logger
from utilities.configurations_constructor.constructor import Constructor


def token_is_correct_format(token: Any) -> Union[bool, TypeError, ValueError, KeyError]:
    """ Helper method, which applies checks whether correct bot token declared in configuration file. """

    if not isinstance(token, str):
        logger.error('TypeError, bot token has to be string.')
        raise TypeError

    if token is None:
        logger.error('ValueError, missing bot token in configurations file.')
        raise ValueError

    if token.isnumeric():
        logger.error('ValueError, bot token contains only "Numbers".')
        raise ValueError

    if token.isalpha():
        logger.error('ValueError, bot token contains only "Alphabets".')
        raise ValueError

    return True


def build(token: str) -> Union[Application, TypeError]:
    """ Helper method, which attempts to build TelegramBot Application. """

    try:
        bot = ApplicationBuilder().token(token).build()
        return bot

    except TypeError:
        logger.error('TypeError, Provided bot token does not exist.')
        raise


def add_handlers(bot: Application) -> Application:
    """ Helper method, which adds telegram_event_handlers to TelegramBot Application. """

    try:
        bot.add_handler(ConversationValidatorHandler)
        bot.add_handler(MemberHandler.handler)
        bot.add_handler(TextMessageHandler.handler)
        bot.add_handler(VideoMessageHandler.handler)
        bot.add_handler(AudioMessageHandler.handler)
        bot.add_handler(DocumentMessageHandler.handler)
    except Exception as error:
        raise f'Exception registered during registering telegram handler. ' \
              f'{error}'

    return bot


def main():
    """ Function, which stands for pre-validating, building and launching `group_eq_bot` application. """

    token = Constructor().configurations.bot.general.token

    if token_is_correct_format(token=token):
        bot = build(token=token)
        bot = add_handlers(bot=bot)
        bot.run_polling()


if __name__ == '__main__':
    main()
