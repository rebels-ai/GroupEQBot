import io
import json
from dataclasses import dataclass, field

from telegram import Update as TelegramEvent, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes, filters, ConversationHandler, MessageHandler, \
    CallbackQueryHandler

from interfaces.models.external_event.event import ReplyKeyboardMarkup
from utilities.internal_logger.logger import logger

from interfaces.models.internal_event.event import ExpectedInternalEvent
from interfaces.telegram_event_handlers.message_update.text.handler import TextMessageHandler

CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

from sentence_transformers import SentenceTransformer

from utilities.configurations_constructor.constructor import Constructor


[SEARCH, BUTTON_PROCESSOR] = range(2)

internal_event: ExpectedInternalEvent
context: ContextTypes.DEFAULT_TYPE
configurator: Constructor = field(default_factory=lambda: Constructor())


from sentence_transformers import SentenceTransformer
# model = SentenceTransformer('all-MiniLM-L6-v2') # see the list of pre-trained models on the https://www.sbert.net/docs/pretrained_models.html
MODEL_NAME = 'symanto/sn-xlm-roberta-base-snli-mnli-anli-xnli'
model = SentenceTransformer(f'{MODEL_NAME}')
from scipy.spatial import distance
filename = 'database.txt'

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

    question = event.message.text
    logger.info('[Search] is called ...')
    # question.replace('#faq', '')
    dbase = open_database(file_name='database.txt')
    embeddings, q_list = create_embeddings(dbase)
    ex_q = find_similar_question(q_list, embeddings, question)
    for item in dbase:
        if item['question'] == ex_q:
            answer_text = item['answers']
            # question_id = 85118  #just for example
            # question_id = item['id']
            # print(type(question_id))
    if len(answer_text) > 0:
        for item in answer_text:
            answer_message = item
            await event.message.reply_text(text=answer_message)
            # from_chat_id = self.internal_event.event.message.from_user.id
            # await self.context.bot.forward_message(chat_id=self.internal_event.event.message.from_user.id, from_chat_id=from_chat_id,
            #                                     message_id=question_id)
    else:
        await event.message.reply_text(text='Ничего не знаю про это')
    #

    reply_keyboard = [
        [
            InlineKeyboardButton(text='Yes', callback_data='Yes'),
            InlineKeyboardButton(text='No', callback_data='No'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(reply_keyboard)
    await event.message.reply_text(text="Скажи, ответ помог?", reply_markup=reply_markup)

    return BUTTON_PROCESSOR


async def button_processor_yes(event: TelegramEvent, context: ContextTypes.DEFAULT_TYPE):
    query = event.callback_query
    await query.answer()

    await query.edit_message_text(
        "Класс! Обращайся еще!"
    )
    logger.info('[Search] is Done succesfully')

    # print(query.answer())
    return ConversationHandler.END

async def button_processor_no(event: TelegramEvent, context: ContextTypes.DEFAULT_TYPE):
    query = event.callback_query
    await query.answer()

    await query.edit_message_text(
        "Очень жаль! Я пока недостаточно хорош :о("
    )
    logger.info('[Search] is not Done well')
    # print(query.answer())
    return ConversationHandler.END



#
async def cancel(event: TelegramEvent, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    # user = event.message.from_user
    # logger.info("User %s canceled the conversation.", user.first_name)
    await event.message.reply_text(
        "Bye! I hope we can talk again some day."
    )
    return ConversationHandler.END


# на команду привязать импут текста, отловить евент, найти в базе, и вернуть ответ из базы


FaqBranchHandler = ConversationHandler(entry_points=[MessageHandler(filters=filters.Regex("#faq"), callback=start_conversation)],
                                  states={
                                      SEARCH: [MessageHandler(filters=filters.TEXT, callback=search_func)],
                                      BUTTON_PROCESSOR: [
                                          CallbackQueryHandler(callback=button_processor_yes, pattern="^"+str('Yes')+"$"),
                                          CallbackQueryHandler(callback=button_processor_no, pattern="^"+str('No')+"$")],
                                  },
                                  fallbacks=[CommandHandler('cancel', cancel)],
                                  )

def open_database(file_name):
    with io.open(file_name, 'r', encoding="utf-8") as f:
        dbase = json.load(f)
    return dbase

def create_embeddings(dbase):

    logger.info(f'[Message][Question] is {dbase[0]}')
    q_list = []
    for item in dbase:
        q_list.append(item['question'])

    embeddings = model.encode(q_list)
    return embeddings, q_list

def find_similar_question(sentences, embeddings, question):
    dists = []
    ques_emb = model.encode(question)
    for sentence, embedding in zip(sentences, embeddings):
        dists.append(distance.cosine(embedding,ques_emb))
    ind = dists.index(min(dists))
    return sentences[ind]