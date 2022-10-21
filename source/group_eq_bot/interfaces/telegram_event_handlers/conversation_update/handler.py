from telegram.ext import ConversationHandler
from interfaces.telegram_event_handlers.conversation_update.constructor.construct import Constructor


entry_points = Constructor().entrypoints
states = Constructor().states
fallbacks = Constructor().fallbacks

ValidatorHandler = ConversationHandler(entry_points=[entry_points],
                                       states=states,
                                       fallbacks=[fallbacks])
