import hydra

from typing import Union, Any
from telegram.ext import ApplicationBuilder, Application

from handlers.chat_member_handler import MemberHandler
from handlers.text_message_handler import TextMessageHandler
from handlers.video_message_handler import VideoMessageHandler
from handlers.audio_message_handler import AudioMessageHandler
from handlers.document_message_handler import DocumentMessageHandler
from handlers.conversation_validation_handler import ConversationValidatorHandler

from internal_logger.logger import logger

HYDRA_VERSION = '1.2'
CONFIGURATIONS_PATH = 'configurations'
CONFIGURATIONS_NAME = 'configuration'


def pre_validate_bot_token(token: Any) -> Union[str, TypeError, ValueError, KeyError]:
    """ Helper method, which applies checks whether correct token declared in configuration file. """

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

    return token


def build_application(token: str) -> Union[Application, TypeError]:
    """ Helper method, which attempts to build TelegramBot Application. """

    try:
        bot = ApplicationBuilder().token(token).build()
        return bot

    except TypeError:
        logger.error('TypeError, Provided bot token does not exist.')
        raise


def add_application_handlers(bot: Application) -> None:
    """ Helper method, which adds handlers to TelegramBot Application. """

    bot.add_handler(ConversationValidatorHandler)
    bot.add_handler(MemberHandler.handler)
    bot.add_handler(TextMessageHandler.handler)
    bot.add_handler(VideoMessageHandler.handler)
    bot.add_handler(AudioMessageHandler.handler)
    bot.add_handler(DocumentMessageHandler.handler)


@hydra.main(version_base=HYDRA_VERSION, config_path=CONFIGURATIONS_PATH, config_name=CONFIGURATIONS_NAME)
def main(configurations):
    """ Function, which stands for pre-validating, building and launching `group_eq_bot` application. """

    pre_validate_bot_token(token=configurations.administration.token)
    bot = build_application(token=configurations.administration.token)
    add_application_handlers(bot=bot)
    bot.run_polling()


if __name__ == '__main__':
    main()
