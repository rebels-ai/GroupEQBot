import hydra

from telegram.ext import ApplicationBuilder

from handlers.chat_member_handler import MemberHandler
from handlers.text_message_handler import TextMessageHandler
from handlers.video_message_handler import VideoMessageHandler
from handlers.audio_message_handler import AudioMessageHandler
from handlers.document_message_handler import DocumentMessageHandler
from handlers.conversation_validation_handler import ConversationValidatorHandler


@hydra.main(version_base='1.1', config_path='configurations', config_name='configuration')
def main(bot_configurations):
    """
    Function, which stands for building and launching group_eq_bot
    with appropriate handlers.
    """

    bot = ApplicationBuilder().token(bot_configurations.administration.token).build()

    bot.add_handler(ConversationValidatorHandler)

    bot.add_handler(MemberHandler.handler)
    bot.add_handler(TextMessageHandler.handler)
    bot.add_handler(VideoMessageHandler.handler)
    bot.add_handler(AudioMessageHandler.handler)
    bot.add_handler(DocumentMessageHandler.handler)

    bot.run_polling()


if __name__ == '__main__':
    main()
