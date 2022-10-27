from dataclasses import dataclass, field

from telegram import Update as TelegramEvent
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler

from utilities.configurations_constructor.constructor import Constructor


@dataclass
class CancelCommandBuilder:
    """ Interface for `cancel_validation` command of ConversationHandler. """

    CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

    handler: CommandHandler = field(init=False)

    command: str = 'cancel_validation'
    callback_return_value: int = ConversationHandler.END
    configurator: Constructor = field(default_factory=lambda: Constructor())

    def __post_init__(self):
        self.handler = [CommandHandler(command=self.command,
                                      callback=self.callback_function)]

    async def callback_function(self, event: TelegramEvent, context: CONTEXT_DEFAULT_TYPE) -> int:
        """ Method, which will be called as a callback for `cancel_validation` command. """

        await event.message.reply_text(text=self.configurator.configurations.bot.validation.validation_canceled_message)
        return self.callback_return_value

