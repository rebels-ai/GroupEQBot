from dataclasses import dataclass
from telegram.ext import CommandHandler, ContextTypes

from telegram import Update as TelegramEvent

from interfaces.telegram_event_router.router import route_event
from utilities.internal_logger.logger import logger


@dataclass
class StartCommandHandler:
    CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

    command_to_be_written = 'start'
    callback_to_call = None

    handler = CommandHandler(command=command_to_be_written,
                             callback=callback_to_call)

    def start(self, event: TelegramEvent, context: CONTEXT_DEFAULT_TYPE) -> int:
        """ Function, which handles `start` command update from CommandHandler. """

        username = event.message.from_user
        logger.info(f'User {username.full_name} started the conversation with bot')
        logger.info(event)

        await event.message.reply_text(text=first_question)

        return FIRST_ANSWER

    def handle(self) -> 'StartCommandHandler':
        self.callback_to_call = self.start()
        return self


@dataclass
class EndCommandHandler:
    command_to_be_written = 'end'
    callback_to_call = route_event

    handler = CommandHandler(command=command_to_be_written,
                             callback=callback_to_call)


@dataclass
class HelpCommandHandler:
    command_to_be_written = 'help'
    callback_to_call = route_event

    handler = CommandHandler(command=command_to_be_written,
                             callback=callback_to_call)
