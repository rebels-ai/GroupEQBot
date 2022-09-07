from dataclasses import dataclass, field
from typing import Optional

from elasticsearch_dsl import Document
from elasticsearch.exceptions import NotFoundError

from utilities.internal_logger.logger import logger

from interfaces.models.internal_event import ExpectedInternalEvent
from storage.schemas.documents.user import User, UserDocument

from storage.connectors.connector import connection


@dataclass
class EventsDatabaseUserInterface:
    """
    Conventions:
        document:
            "internal_event.user_id" - stands for "_id" of the elasticsearch document.
        index:
            "index is dynamically generated as" - <bot.configs.name>-<bot.configs.version>-user-chatID-userID
    """

    DOCUMENT_KEY = "doc"

    internal_event: ExpectedInternalEvent
    document: UserDocument = field(init=False)
    document_id: int = field(init=False)
    index: str = field(init=False)

    def __post_init__(self):
        self.document = self.generate_user_document_model()
        self.document_id = self.set_document_id()
        # reference to UserDocument index convention: <bot.configs.name>-<bot.configs.version>-user-chatID-userID
        self.index = f'{self.document.Index.name}-{abs(self.internal_event.chat_id)}-{self.internal_event.user_id}'

    def set_document_id(self) -> int:
        """ Method to set elasticsearch document id. """
        return self.internal_event.user_id

    def generate_user_model(self) -> User:
        """
        Function, which generates User data model
        based on User schema.
        """

        try:
            data_model = User(user_id=self.internal_event.user_id,
                              first_name=self.internal_event.first_name,
                              last_name=self.internal_event.last_name,
                              username=self.internal_event.username)
        except Exception as error:
            logger.warning('Failed User model generation.')
            raise error

        return data_model

    def generate_user_document_model(self) -> UserDocument:
        """
        Function, which generates UserDocument data model
        based on User schema.
        """

        try:
            data_model = UserDocument(meta={'id': self.document_id},
                                      user=self.generate_user_model())

        except Exception as error:
            logger.warning('Failed UserDocument model generation.')
            raise error

        return data_model

    def get_document_from_index(self) -> Optional[Document]:
        """ Function, which reads document by index and documentID. """

        try:
            document_from_database = self.document.get(index=self.index, id=self.internal_event.user_id)
            return document_from_database

        except NotFoundError: 
            return

    def user_first_name_matches(self, document: Document) -> bool:
        """ Function, which checks whether EventUserFirstName equals DocumentUserFirstName. """
        return True if document.user.first_name == self.internal_event.first_name else False

    def user_last_name_matches(self, document: Document) -> bool:
        """ Function, which checks whether EventUserLastName equals DocumentUserLastName. """
        return True if document.user.last_name == self.internal_event.last_name else False

    def username_matches(self, document: Document) -> bool:
        """ Function, which checks whether EventUsername equals DocumentUsername. """
        return True if document.user.username == self.internal_event.username else False

    def process(self):
        """ Entrypoint to EventsDatabaseUserInterface, holding the main logic. """

        logger.info(f'[EventsDatabaseUserInterface] INDEX NAME -- {self.index} ')

        # either index does not exist at all
        # or document does not exist
        document_from_database = self.get_document_from_index()
        if document_from_database is None:
            self.document.save(index=self.index)
            return
        
        first_name_match = self.user_first_name_matches(document=document_from_database)
        last_name_match = self.user_last_name_matches(document=document_from_database)
        username_match = self.username_matches(document=document_from_database)

        if not first_name_match or not last_name_match or not username_match:
            connection.update(index=self.index,
                              id=self.document_id,
                              body={self.DOCUMENT_KEY: self.document})
            return

        return
