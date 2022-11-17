from dataclasses import dataclass

from telegram import Update as TelegramEvent
from telegram.ext import ContextTypes


@dataclass
class StartHelper:
    """ Helper methods for StartCommandHandler """

    CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

    event: TelegramEvent
    context: CONTEXT_DEFAULT_TYPE

    async def chat_owner(self, chat_id: str) -> bool:
        """ Method, which checks whether message author is a chat owner. """

        member = await self.context.bot.get_chat_member(
            chat_id=-int(chat_id),
            user_id=self.event.effective_user.id
            )

        return True if member.status == 'creator' else False
