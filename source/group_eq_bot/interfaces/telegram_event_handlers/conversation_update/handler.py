from telegram.ext import ConversationHandler
from constructor.construct import HandlerConstructor


ValidatorHandler = ConversationHandler(HandlerConstructor.build())