from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from elasticsearch_dsl import Document
from elasticsearch.exceptions import NotFoundError
from utilities.internal_logger.logger import logger

from interfaces.models.internal_event.event import ExpectedInternalEvent
from storage.schemas.documents.user import User, UserDocument

from storage.connectors.connector import connection


@dataclass
class EventsDatabaseUserInterface:
    """ Main EventsDatabase interface for events.user related R/W operations.

    Notes:
        The conventions:
            Index:
                in terms of event, "index is dynamic":
                    <bot.configs.name>-<bot.configs.version>-user-<chatID>-<userID>
            DocumentID:
                in terms of event, "document id is dynamic":
                    internal_event.user_id - stands for "_id" of the elasticsearch document.
    """

    DOCUMENT_KEY = "doc"  # required elasticsearch document (inside index) key, to find body for update method

    internal_event: ExpectedInternalEvent

    index: str = field(init=False)  # database index name
    document_id: int = field(init=False)  # database index document id
    document: UserDocument = field(init=False)  # database index document object

    def __post_init__(self):
        self.document_id = self.set_document_id()
        self.document = self.generate_user_document_model()

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
                              username=self.internal_event.username,
                              last_activity=datetime.now())  # @NOTE: last activity supposed to be taken from internal_event.event_time

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
        return True if self.internal_event.first_name in document.user.first_name else False

    def user_last_name_matches(self, document: Document) -> bool:
        """ Function, which checks whether EventUserLastName equals DocumentUserLastName. """
        return True if self.internal_event.last_name in document.user.last_name else False

    def username_matches(self, document: Document) -> bool:
        """ Function, which checks whether EventUsername equals DocumentUsername. """
        return True if self.internal_event.username in document.user.username else False

    def process(self):
        """ Entrypoint to EventsDatabaseUserInterface, holding the main logic. """

        logger.info(f'[EventsDatabaseUserInterface] INDEX NAME -- {self.index} ')

        # either index does not exist at all or document with self.internal_event.user_id does not exist
        document_from_database = self.get_document_from_index()
        if document_from_database is None:
            self.document.save(index=self.index)
            return

        # check if first_name | last_name | username | current_status has changed
        # if yes, update certain field for document from database
        if not self.user_first_name_matches(document=document_from_database):
            registered_first_names = document_from_database.user.first_name

            if isinstance(registered_first_names, str):
                document_from_database.user.first_name = [document_from_database.user.first_name, self.document.user.first_name]
            else:
                document_from_database.user.first_name.append(self.document.user.first_name) 

        if not self.user_last_name_matches(document=document_from_database):
            registered_last_names = document_from_database.user.last_name

            if isinstance(registered_last_names, str):
                document_from_database.user.last_name = [document_from_database.user.last_name, self.document.user.last_name]
            else:
                document_from_database.user.last_name.append(self.document.user.last_name)

        if not self.username_matches(document=document_from_database):
            registered_usernames = document_from_database.user.username

            if isinstance(registered_usernames, str):
                document_from_database.user.username = [document_from_database.user.username, self.document.user.username]
            else:
                document_from_database.user.username.append(self.document.user.username)

        document_from_database.user.last_activity = datetime.now()
        connection.update(index=self.index,
                          id=self.document_id,
                          body={self.DOCUMENT_KEY: document_from_database})

        return
