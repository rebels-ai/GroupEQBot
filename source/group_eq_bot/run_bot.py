from typing import List, Union, Any
from dataclasses import dataclass, field

from telegram import Update
from telegram.ext import ApplicationBuilder, Application

from utilities.internal_logger.logger import logger
from utilities.configurations_constructor.constructor import Constructor


@dataclass
class BotBuilder:
    token: Any = field(init=True)
    bot: Application = field(init=False)
    allowed_updates: List = field(default_factory=lambda: Update.ALL_TYPES)  # mandatory to specify parameter to catch all the telegram updates

    def __post_init__(self):
        self._token_is_correct_format()
        self.__build()
        self.__add_handlers()

    def _token_is_correct_format(self) -> Union[None, TypeError, ValueError, KeyError]:
        """ Helper method, which applies checks whether correct bot token declared in configuration file. """

        if not isinstance(self.token, str):
            logger.error('TypeError, bot token has to be string.')
            raise TypeError

        if self.token is None:
            logger.error('ValueError, missing bot token in configurations file.')
            raise ValueError

        if self.token.isnumeric():
            logger.error('ValueError, bot token contains only "Numbers".')
            raise ValueError

        if self.token.isalpha():
            logger.error('ValueError, bot token contains only "Alphabets".')
            raise ValueError

        return

    def _add_bot_handler(self):
        from interfaces.telegram_event_handlers.bot_update.handler import BotHandler
        self.bot.add_handler(BotHandler.handler)

    def _add_start_validation_handler(self):
        from interfaces.telegram_event_handlers.conversation_update.commands.start import StartValidation
        self.bot.add_handler(StartValidation.handler)

    def _add_member_handler(self):
        from interfaces.telegram_event_handlers.member_update.handler import MemberHandler
        self.bot.add_handler(MemberHandler.handler)

    def _add_text_handler(self):
        from interfaces.telegram_event_handlers.message_update.text.handler import TextMessageHandler
        self.bot.add_handler(TextMessageHandler.handler)

    def _add_video_handler(self):
        from interfaces.telegram_event_handlers.message_update.video.handler import VideoMessageHandler
        self.bot.add_handler(VideoMessageHandler.handler)

    def _add_audio_handler(self):
        from interfaces.telegram_event_handlers.message_update.audio.handler import AudioMessageHandler
        self.bot.add_handler(AudioMessageHandler.handler)

    def _add_document_handler(self):
        from interfaces.telegram_event_handlers.message_update.document.handler import DocumentMessageHandler
        self.bot.add_handler(DocumentMessageHandler.handler)

    def _add_validation_handler(self):
        from interfaces.telegram_event_handlers.conversation_update.handler import ValidatorHandler
        self.bot.add_handler(ValidatorHandler)

    def __add_handlers(self):
        """ Helper method, which adds telegram_event_handlers to TelegramBot Application. """

        self._add_validation_handler()
        self._add_start_validation_handler()
        self._add_bot_handler()
        self._add_video_handler()
        self._add_audio_handler()
        self._add_text_handler()
        self._add_member_handler()
        self._add_document_handler()

    def __build(self):
        """ Method, which attempts to build TelegramBot Application. """
        try:
            self.bot = ApplicationBuilder().token(self.token).build()
        except TypeError:
            logger.error('TypeError, Provided bot token does not exist.')
            raise

    def launch(self):
        self.bot.run_polling(allowed_updates=self.allowed_updates)


def main():
    """ Function, which stands for pre-validating, building and launching `group_eq_bot` application. """
    token = Constructor().configurations.bot.general.token
    BotBuilder(token=token).launch()


if __name__ == '__main__':
    main()
