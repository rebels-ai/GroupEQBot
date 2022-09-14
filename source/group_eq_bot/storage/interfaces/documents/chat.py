from dataclasses import dataclass, field
from typing import Optional

from elasticsearch_dsl import Document
from elasticsearch.exceptions import NotFoundError

from utilities.internal_logger.logger import logger

from interfaces.models.internal_event.event import ExpectedInternalEvent
from storage.schemas.documents.chat import Chat, ChatDocument

from storage.connectors.connector import connection


@dataclass
class EventsDatabaseChatInterface:
    """
    Main EventsDatabase interface for events.chat related R/W operations.

    Notes:
        The conventions:
            Index:
                in terms of event, "index is static":
                    <bot.configs.name>-<bot.configs.version>-chats-name-id-mappings
            DocumentID:
                in terms of event, "document id is dynamic":
                    abs(internal_event.chat_id) - stands for "_id" of the elasticsearch document.
    """

    INDEX_POSTFIX_CONVENTION = 'chats-name-id-mappings'
    DOCUMENT_KEY = "doc"  # required elasticsearch document (inside index) key, to find body for update method

    internal_event: ExpectedInternalEvent

    index: str = field(init=False)  # database index name
    document_id: int = field(init=False)  # database index.document id
    document: ChatDocument = field(init=False)  # database index.document object

    def __post_init__(self):
        self.document_id = self.set_document_id()
        self.document = self.generate_chat_document_model()
        self.index = f'{self.document.Index.name}-{self.INDEX_POSTFIX_CONVENTION}'

    def set_document_id(self) -> int:
        """ Method to set elasticsearch document id. """
        return abs(self.internal_event.chat_id)

    def generate_chat_model(self) -> Chat:
        """ Function, which generates Chat data model based on Chat schema. """

        try:
            # @NOTE: required filed changes,
            # because Elasticsearch does not support custom types
            _id = self.document_id
            _name = self.internal_event.chat_name
            _type = self.internal_event.chat_type
            user_id = str(self.internal_event.user_id)

            data_model = Chat(chat_id=_id,
                              chat_name=_name,
                              chat_type=_type,
                              chat_historic_members=user_id)

        except Exception as error:
            logger.warning('Failed Chat model generation.')
            raise error

        return data_model

    def generate_chat_document_model(self) -> ChatDocument:
        """ Function, which generates ChatDocument data model based on Chat schema. """

        try:
            data_model = ChatDocument(meta={'id': self.document_id},
                                      chat=self.generate_chat_model())

        except Exception as error:
            logger.warning('Failed ChatDocument model generation.')
            raise error

        return data_model

    def get_document_from_index(self) -> Optional[Document]:
        """ Function, which reads document by index and documentID. """

        try:
            document_from_database = self.document.get(index=self.index,
                                                       id=abs(self.internal_event.chat_id))
            return document_from_database

        except NotFoundError: 
            return

    def chat_name_matches(self, document: Document) -> bool:
        """ Helper function, which checks whether EventChatName equals DocumentChatName. """
        return True if self.document.chat.chat_name in document.chat.chat_name else False

    def chat_type_matches(self, document: Document) -> bool:
        """ Helper function, which checks whether EventChatType equals DocumentChatType. """
        return True if self.document.chat.chat_type in document.chat.chat_type else False

    def user_is_already_registered_in_chat(self, document: Document) -> bool:
        """ Helper function, which checks whether EventUserID is in Document. """
        return True if self.document.chat.chat_historic_members in document.chat.chat_historic_members else False

    def process(self):
        """ Entrypoint to EventsDatabaseChatInterface, holding the main logic. """

        logger.info(f'[EventsDatabaseChatInterface] INDEX NAME -- {self.index} ')

        document_from_database = self.get_document_from_index()
        if document_from_database is None:
            self.document.save(index=self.index)
            return

        # check if chat_name | chat_type | chat_historic_members has changed
        # if yes, update certain field for document from database
        change_happened = False
        if not self.chat_name_matches(document=document_from_database):
            change_happened = True
            registered_chat_names = document_from_database.chat.chat_name

            if isinstance(registered_chat_names, str):
                document_from_database.chat.chat_name = [document_from_database.chat.chat_name,
                                                         self.document.chat.chat_name]
            else:
                document_from_database.chat.chat_name.append(self.document.chat.chat_name)

        if not self.chat_type_matches(document=document_from_database):
            change_happened = True
            registered_chat_types = document_from_database.chat.chat_type

            if isinstance(registered_chat_types, str):
                document_from_database.chat.chat_type = [document_from_database.chat.chat_type,
                                                         self.document.chat.chat_type]
            else:
                document_from_database.chat.chat_type.append(self.document.chat.chat_type)

        if not self.user_is_already_registered_in_chat(document=document_from_database):
            change_happened = True
            registered_user_ids = document_from_database.chat.chat_historic_members

            if isinstance(registered_user_ids, str):
                document_from_database.chat.chat_historic_members = [document_from_database.chat.chat_historic_members,
                                                                     self.document.chat.chat_historic_members]
            else:
                document_from_database.chat.chat_historic_members.append(self.document.chat.chat_historic_members)

        if change_happened:
            connection.update(index=self.index,
                              id=self.document_id,
                              body={self.DOCUMENT_KEY: document_from_database})
        return
