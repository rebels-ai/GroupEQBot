from telegram.ext import ConversationHandler
from interfaces.telegram_event_handlers.conversation_update.constructor.construct import Constructor


# Constructor.states
# Constructor.entrypoint
# Constructor.fallbacks

ValidatorHandler = ConversationHandler(entry_points=Constructor().entrypoints,
                                       states=Constructor().states,
                                       fallbacks=Constructor().fallbacks)
