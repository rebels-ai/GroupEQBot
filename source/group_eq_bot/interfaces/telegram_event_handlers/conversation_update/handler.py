from telegram.ext import ConversationHandler
from constructor.construct import Constructor


# Constructor.states
# Constructor.entrypoint
# Constructor.fallbacks

ValidatorHandler = ConversationHandler(entry_points=Constructor().entrypoint,
                                       states=Constructor().states,
                                       fallbacks=Constructor().fallbacks)
