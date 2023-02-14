from dataclasses import dataclass, field

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from utilities.internal_logger.logger import logger
from utilities.configurations_constructor.constructor import Constructor

from interfaces.models.internal_event.member_status import MemberStatus
from interfaces.models.internal_event.event import ExpectedInternalEvent

#well...
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2') # see the list of pre-trained models on the https://www.sbert.net/docs/pretrained_models.html
from scipy.spatial import distance
import json
import io
file_name = 'database.txt'

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


@dataclass
class MessageEventProcessor:
    """ Main Interface to process private messages.

    Constraint:
        Interface is supposed to be executed JUST and only in the use case,
        when bot has been started by user in 1:1 private chat
    """

    internal_event: ExpectedInternalEvent
    context: ContextTypes.DEFAULT_TYPE
    configurator: Constructor = field(default_factory=lambda: Constructor())

    async def process(self) -> None:
        """ Entrypoint for the MessageEventProcessor, which based on the bot StatusChange event, invoke appropriate logic. """

        logger.info('[MessageEventProcessor] is called ...')

        # User send private message to bot
        if '#faq' in self.internal_event.message:

            await self.context.bot.send_message(chat_id=self.internal_event.event.message.from_user.id,
                                                text=self.configurator.configurations.bot.talks.faqing)
            question = self.internal_event.message
            question.replace('#faq', '')
            dbase = open_database(file_name)
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
                    await self.context.bot.send_message(chat_id=self.internal_event.event.message.from_user.id,
                                                    text=answer_message)
                    # from_chat_id = self.internal_event.event.message.from_user.id
                    # await self.context.bot.forward_message(chat_id=self.internal_event.event.message.from_user.id, from_chat_id=from_chat_id,
                    #                                     message_id=question_id)
            else:
                await self.context.bot.send_message(chat_id=self.internal_event.event.message.from_user.id,
                                                    text=self.configurator.configurations.bot.talks.idontknow)


            reply_markup = self._get_reply_markup()
            await self.context.bot.send_message(chat_id=self.internal_event.event.message.from_user.id, text=self.configurator.configurations.bot.talks.wasitusefull, reply_markup=reply_markup)
            # if self.internal_event.message:
        # else:
        #     logger.info(f'[UNEXPECTED EVENT] bot was {self.internal_event.old_status}, became {self.internal_event.new_status}')
        return

    def _get_reply_markup(self):
        keyboard = [
            [
                InlineKeyboardButton(text=self.configurator.configurations.bot.talks.itwasusefull, callback_data='Yes'),
                InlineKeyboardButton(text=self.configurator.configurations.bot.talks.itwasnotusefull, callback_data='No'),
            ]
        ]
        return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True,
                                       resize_keyboard=True)
