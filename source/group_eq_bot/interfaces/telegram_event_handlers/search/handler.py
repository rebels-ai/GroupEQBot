from dataclasses import dataclass, field

from telegram import Update as TelegramEvent, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ContextTypes, filters, ConversationHandler, MessageHandler

from interfaces.models.external_event.event import InlineKeyboardButton, ReplyKeyboardMarkup
from utilities.internal_logger.logger import logger

from interfaces.models.internal_event.event import ExpectedInternalEvent
from interfaces.telegram_event_handlers.message_update.text.handler import TextMessageHandler

CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

from sentence_transformers import SentenceTransformer

from utilities.configurations_constructor.constructor import Constructor


[SEARCH, BUTTON_PROCESSOR] = range(2)

@dataclass
class SearchHandler:
    """ Handler builder for search functionality """

    internal_event: ExpectedInternalEvent
    context: ContextTypes.DEFAULT_TYPE
    configurator: Constructor = field(default_factory=lambda: Constructor())
    command: str = 'search'
    # filename = 'database.txt'

    async def start_conversation(event: TelegramEvent, context: ContextTypes.DEFAULT_TYPE):
        await event.message.reply_text(text='Привет! Задай свой вопрос')
        # await event.message.reply
        return SEARCH
    # async def start_conversation(internal_event: ExpectedInternalEvent, context: ContextTypes.DEFAULT_TYPE):
    #     await context.bot.send_message(chat_id=internal_event.event.message.from_user.id,
    #                                         text='Привет! Задай свой вопрос')
    #     return SEARCH
    #
    async def search_func(event: TelegramEvent, context: ContextTypes.DEFAULT_TYPE):
    #     #
        question = event.message.text
    #     logger.info('[Search] is called ...')
    #     # question.replace('#faq', '')
    #     dbase = open_database(file_name)
    #     embeddings, q_list = create_embeddings(dbase)
    #     ex_q = find_similar_question(q_list, embeddings, question)
    #     for item in dbase:
    #         if item['question'] == ex_q:
        #         answer_text = item['answers']
        #         # question_id = 85118  #just for example
        #         # question_id = item['id']
        #         # print(type(question_id))
        # if len(answer_text) > 0:
        #     for item in answer_text:
        #         answer_message = item
        #         await self.context.bot.send_message(chat_id=self.internal_event.event.message.from_user.id,
        #                                         text=answer_message)
        #         # from_chat_id = self.internal_event.event.message.from_user.id
        #         # await self.context.bot.forward_message(chat_id=self.internal_event.event.message.from_user.id, from_chat_id=from_chat_id,
        #         #                                     message_id=question_id)
        # else:
        #     await self.context.bot.send_message(chat_id=self.internal_event.event.message.from_user.id,
        #                                         text=self.configurator.configurations.bot.talks.idontknow)
        #
        #
        reply_keyboard = [
            [
                InlineKeyboardButton(text=self.configurator.configurations.bot.talks.itwasusefull, callback_data='Yes'),
                InlineKeyboardButton(text=self.configurator.configurations.bot.talks.itwasnotusefull, callback_data='No'),
            ]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard=reply_keyboard)
        await event.message.reply_text('Вот что я нашел: ',reply_markup=reply_markup)
    #     #
    #     # # else:
    #     # #     logger.info(f'[UNEXPECTED EVENT] bot was {self.internal_event.old_status}, became {self.internal_event.new_status}')
    #
        return BUTTON_PROCESSOR
    #
    #
    #
    #
    #
    async def button_processor():
        if event.message.text == "Yes":
            logger.info('[Search] is Done succesfully')
            return ConversationHandler.END
        else:
            logger.info('[Search] is not Done well')
            return ConversationHandler.END
    #
    async def cancel(event: TelegramEvent, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancels and ends the conversation."""
        # user = event.message.from_user
        # logger.info("User %s canceled the conversation.", user.first_name)
        await event.message.reply_text(
            "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    handler = ConversationHandler(entry_points=[CommandHandler(command='search', callback=start_conversation)],
                                  states={
                                      SEARCH: [MessageHandler(filters=filters.TEXT, callback=search_func)],
                                      BUTTON_PROCESSOR: [MessageHandler(filters=filters.TEXT, callback=button_processor)],
                                  },
                                  fallbacks=[CommandHandler('cancel', cancel)],
                                  )
# на команду привязать импут текста, отловить евент, найти в базе, и вернуть ответ из базы


