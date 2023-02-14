import io
import json
from dataclasses import field

from telegram import Update as TelegramEvent, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, ContextTypes, filters, ConversationHandler, MessageHandler, \
    CallbackQueryHandler

from utilities.internal_logger.logger import logger

from interfaces.models.internal_event.event import ExpectedInternalEvent

CONTEXT_DEFAULT_TYPE = ContextTypes.DEFAULT_TYPE

from utilities.configurations_constructor.constructor import Constructor

[SEARCH, BUTTON_PROCESSOR] = range(2)

internal_event: ExpectedInternalEvent
context: ContextTypes.DEFAULT_TYPE
configurator: Constructor = field(default_factory=lambda: Constructor())

from sentence_transformers import SentenceTransformer

MODEL_NAME = 'symanto/sn-xlm-roberta-base-snli-mnli-anli-xnli'
model = SentenceTransformer(f'{MODEL_NAME}')
from scipy.spatial import distance

filename = 'database.txt'


async def start_conversation(event: TelegramEvent, context: ContextTypes.DEFAULT_TYPE):
    await event.message.reply_text(text='Привет! Задай свой вопрос')
    return SEARCH


async def search_func(event: TelegramEvent, context: ContextTypes.DEFAULT_TYPE):
    question = event.message.text
    logger.info('[Search] is called ...')
    dbase = open_database(file_name='database.txt')

    answers_and_indexes = find_n_similar_questions_from_presaved_embaddings(dbase, question, deps=3)
    final_answers = give_n_answers(dbase, answers_and_indexes)
    print(final_answers)
    for item in final_answers:
        await event.message.reply_text(text=item[0])

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

    return ConversationHandler.END

async def button_processor_no(event: TelegramEvent, context: ContextTypes.DEFAULT_TYPE):
    query = event.callback_query
    await query.answer()

    await query.edit_message_text(
        "Очень жаль! Я пока недостаточно хорош :о("
    )
    logger.info('[Search] is not Done well')
    return ConversationHandler.END


#
async def cancel(event: TelegramEvent, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""

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
                                    conversation_timeout=30,
                                  )

def open_database(file_name):
    with io.open(file_name, 'r', encoding="utf-8") as f:
        dbase = json.load(f)
    return dbase


def find_n_similar_questions_from_presaved_embaddings(dbase, question, deps=10):
    dists = []
    question_embedding = model.encode(question)
    for item in dbase:
        dists.append(distance.cosine(item['embedding'], question_embedding))
    ans_n_index_list = []
    i = 0
    while i < deps:
        min_dist = min(dists)
        ind = dists.index(min_dist)
        ans_n_index_list.append((ind, min_dist))
        dists.remove(min_dist)
        i += 1
    return ans_n_index_list

def give_n_answers(database, answers_n_indexs):
    what_to_say = []
    for row in answers_n_indexs:
        q = database[row[0]]['question']
        mlink = database[row[0]]['message_url']
        answer_message = f'Кажется здесь {mlink} уже шла речь об этом: \n {q} \n Distance: {row[1]}'
        what_to_say.append([answer_message, database[row[0]]['id']])
    return what_to_say
