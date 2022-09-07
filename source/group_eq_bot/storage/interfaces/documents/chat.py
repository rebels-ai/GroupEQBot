from dataclasses import dataclass, field
from typing import Optional

from elasticsearch_dsl import Document, UpdateByQuery
from elasticsearch.exceptions import NotFoundError

from utilities.internal_logger.logger import logger

from interfaces.models.internal_event import ExpectedInternalEvent
from storage.schemas.documents.chat import Chat, ChatDocument

from storage.connectors.connector import connection


@dataclass
class EventsDatabaseChatInterface:
    """
    Conventions:
        document:
            "internal_event.chat_id" - stands for "_id" of the elasticsearch document.
        index:
            "index is dynamically generated as" - <bot.configs.name>-<bot.configs.version>-chats-name-id-mappings
    """

    INDEX_POSTFIX_CONVENTION = 'chats-name-id-mappings'

    internal_event: ExpectedInternalEvent
    document: ChatDocument = field(init=False)
    index: str = field(init=False)

    def __post_init__(self):
        self.document = self.generate_chat_document_model()
        # reference to ChatDocument index convention: <bot.configs.name>-<bot.configs.version>-chats-name-id-mappings
        self.index = f'{self.document.Index.name}-{self.INDEX_POSTFIX_CONVENTION}'

    def generate_chat_model(self) -> Chat:
        """
        Function, which generates Chat data model
        based on Chat schema.
        """

        try:
            # @Note: required filed changes,
            # because Elasticsearch does not support custom types
            _id = abs(self.internal_event.chat_id)
            _name = self.internal_event.chat_name
            _type = self.internal_event.chat_type

            data_model = Chat(chat_id=_id,
                              chat_name=_name,
                              chat_type=_type)
        except Exception as error:
            logger.warning('Failed Chat model generation.')
            raise error

        return data_model

    def generate_chat_document_model(self) -> ChatDocument:
        """
        Function, which generates ChatDocument data model
        based on Chat schema.
        """

        try:
            data_model = ChatDocument(meta={'id': abs(self.internal_event.chat_id)},
                                      chat=self.generate_chat_model())

        except Exception as error:
            logger.warning('Failed ChatDocument model generation.')
            raise error

        return data_model

    def get_document_from_index(self) -> Optional[Document]:
        """ Function, which reads document by index and documentID. """

        try:
            document_from_database = self.document.get(index=self.index, id=abs(self.internal_event.chat_id))
            return document_from_database

        except NotFoundError: 
            return

    def chat_name_matches(self, document: Document) -> bool:
        """ Function, which checks whether EventChatName equals DocumentChatName. """
        return True if document.chat.chat_name == self.internal_event.chat_name else False

    def chat_type_matches(self, document: Document) -> bool:
        """ Function, which checks whether EventChatType equals DocumentChatType. """
        return True if document.chat.chat_type == self.internal_event.chat_type else False

    def process(self):
        """ Entrypoint to EventsDatabaseChatInterface, holding the main logic. """

        logger.info(f'[EventsDatabaseChatInterface] INDEX NAME -- {self.index} ')

        # either index does not exist at all
        # or document does not exist
        document_from_database = self.get_document_from_index()
        if document_from_database is None:
            self.document.save(index=self.index)
            return

        chat_name_match = self.chat_name_matches(document=document_from_database)
        chat_type_match = self.chat_type_matches(document=document_from_database)

        if not chat_name_match and not chat_type_match:

            connection.update(index=self.index,
                              id=document_from_database.chat.chat_id,
                              )

            # self.document.update(index=self.index,
            #                      detect_noop=False,
            #                      refresh=True,
            #                      doc_as_upsert=True,
            #                      chat_name=self.internal_event.chat_name,
            #                      chat_type=self.internal_event.chat_type)
            return

        elif not chat_name_match:
            # self.document.update(index=self.index,
            #                      detect_noop=False,
            #                      refresh=True,
            #                      doc_as_upsert=True,
            #                      chat_name=self.internal_event.chat_name)

            connection.update(index=self.index,
                              id=document_from_database.chat.chat_id,
                              body={
                                "doc": self.document
                              })

            return

        elif not chat_type_match:
            self.document.update(index=self.index,
                                 detect_noop=False,
                                 refresh=True,
                                 doc_as_upsert=True,
                                 chat_type=self.internal_event.chat_type)
            return

        return
