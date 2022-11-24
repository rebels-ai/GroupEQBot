from dataclasses import dataclass
from telegram.ext import CommandHandler

from interfaces.telegram_event_handlers.conversation_update.commands.helper import check_validation_status


@dataclass
class StartValidationHandler:
    command: str = 'start_validation'
    callback_to_call = check_validation_status

    handler = CommandHandler(command=command,
                             callback=callback_to_call)
