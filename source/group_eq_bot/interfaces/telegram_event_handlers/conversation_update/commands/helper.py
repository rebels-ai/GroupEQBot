from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update as TelegramEvent
from telegram.ext import ContextTypes
from elasticsearch_dsl import Q

from storage.schemas.group_users.schema import GroupUser
from storage.schemas.chats_mappings.schema import ChatsMapping
from storage.query.query import search_in_existing_index
from utilities.configurations_constructor.constructor import Constructor


configurator = Constructor()
CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

async def check_validation_status(event: TelegramEvent, context: CONTEXT_DEFAULT_TYPE):
    """ Callback function for /start_validation command. 
        Query the database for checking user's chats where they hasn't yet validated
        and generate buttons for available options. """

    user_id = event.effective_user.id
    query = Q('match', user_id=user_id)
    index_name = f'{GroupUser.Index.name}-group-users-*'
    user_documents = search_in_existing_index(query=query, index_name=index_name, doc_type=GroupUser)
    user_not_passed = []

    # User is not presented in any chats where bot is added
    # @NOTE: Or user was in the group before the bot was added --> will be obsolete when fetch_users method implemented
    if len(user_documents.hits) == 0:
        await event.message.reply_text(text=configurator.configurations.bot.validation.user_not_found)

    else:
        for doc in user_documents.hits:
            if doc.event.validation.passed == False:
                user_not_passed.append(doc.meta.index.replace(f'{GroupUser.Index.name}-group-users-', ''))

        if len(user_not_passed) == 0:
            await event.message.reply_text(text=configurator.configurations.bot.validation.already_passed)
        else:
            index_name = f'{ChatsMapping.Index.name}-chats-name-id-mappings'
            chat_mappings = {}
            for chat in user_not_passed:
                chats_query = Q('match', chat_id=chat)
                response = search_in_existing_index(query=chats_query, index_name=index_name, doc_type=ChatsMapping)
                for hit in response.hits:
                    d = {hit.chat_name: chat}
                    chat_mappings.update(d)
            
            keyboard = []
            for name, id in chat_mappings.items():
                button = [InlineKeyboardButton(text=name, callback_data=id)]
                keyboard.append(button)

            validation_options = InlineKeyboardMarkup(keyboard)

            await event.message.reply_text(reply_markup=validation_options,
                                           text=configurator.configurations.bot.validation.start_message_with_buttons)
