from dataclasses import dataclass, field

from group_eq_bot.utilities.internal_logger.logger import logger

from group_eq_bot.storage.schemas.documents.chat import Chat
from group_eq_bot.storage.schemas.documents.user import User
from group_eq_bot.storage.schemas.documents.event import EventDocument, EventMetadata, Event
from group_eq_bot.interfaces.models.internal_event import ExpectedInternalEvent

from group_eq_bot.storage.connectors.connector import connection


@dataclass
class EventsDatabaseEventInterface:
    """
    Conventions:
        document:
            "internal_event.user_id" - stands for "_id" of the elasticsearch document.
        index:
            "index is dynamically generated as" - <bot.configs.name>-<bot.configs.version>-event-chatID-userID
    """

    internal_event: ExpectedInternalEvent
    document: EventDocument = field(init=False)
    index: str = field(init=False)

    def generate_event_metadata_model(self) -> EventMetadata:
        """
        Function, which generates EventMetadata data model
        based on EventMetadata schema.
        """

        try:
            data_model = EventMetadata(event_type=self.internal_event.event_type,
                                       event_time=self.internal_event.event_time)
        except Exception as error:
            logger.warning('Failed EventMetadata model generation.')
            raise error

        return data_model

    def generate_chat_metadata_model(self) -> Chat:
        """
        Function, which generates ChatMetadata data model
        based on Chat schema.
        """

        try:
            data_model = Chat(chat_id=abs(self.internal_event.chat_id),
                              chat_name=self.internal_event.chat_name,
                              chat_type=self.internal_event.chat_type)
        except Exception as error:
            logger.warning('Failed ChatMetadata model generation.')
            raise error

        return data_model

    def generate_user_metadata_model(self) -> User:
        """
        Function, which generates UserMetadata data model
        based on Chat schema.
        """

        try:
            data_model = User(user_id=self.internal_event.user_id,
                              first_name=self.internal_event.first_name,
                              last_name=self.internal_event.last_name,
                              username=self.internal_event.username)
        except Exception as error:
            logger.warning('Failed UserMetadata model generation.')
            raise error

        return data_model

    def generate_event_model(self) -> Event:
        """
        Function, which generates Event data model
        based on Chat, User, EventMetadata schemas.
        """

        try:
            data_model = Event(raw_event=self.internal_event.dict(),
                               event_metadata=self.generate_event_metadata_model(),
                               chat_metadata=self.generate_chat_metadata_model(),
                               user_metadata=self.generate_user_metadata_model(),
                               message_id=str(self.internal_event.message_id),
                               content=self.internal_event.message)
        except Exception as error:
            logger.warning('Failed Event model generation.')
            raise error

        return data_model

    def generate_event_document_model(self) -> EventDocument:
        """
        Function, which generates EventDocument data model
        based on Chat, User, EventMetadata schemas.

        Notes:
            The final data model used for Elasticsearch-dsl interface.
        """

        try:
            data_model = EventDocument(event=self.generate_event_model())
        except Exception as error:
            logger.warning('Failed Event model generation.')
            raise error

        return data_model

    def align_event_type_for_raw_event(self):
        """
        Function, which aligns ExpectedInternalEvent data model event_type field.

        Notes:
            The model with aligned event_type field,
            because Elasticsearch does not accept custom types.
        """
        self.internal_event.event_type = self.internal_event.event_type.value

    def align_chat_type_for_raw_event(self):
        """
        Function, which aligns ExpectedInternalEvent data model chat_type field.

        Notes:
            The model with aligned chat_type field,
            because Elasticsearch does not accept custom types.
        """
        self.internal_event.chat_type = self.internal_event.chat_type.value

    def align_new_member_status_for_raw_event(self):
        """
        Function, which aligns ExpectedInternalEvent data model new_member_status field.

        Notes:
            The model with aligned chat_type field,
            because Elasticsearch does not accept custom types.
        """
        self.internal_event.new_status = self.internal_event.new_status.value

    def align_old_member_status_for_raw_event(self):
        """
        Function, which aligns ExpectedInternalEvent data model new_member_status field.

        Notes:
            The model with aligned chat_type field,
            because Elasticsearch does not accept custom types.
        """
        self.internal_event.old_status = self.internal_event.old_status.value

    def __post_init__(self):
        self.align_event_type_for_raw_event()
        self.align_chat_type_for_raw_event()
        self.align_new_member_status_for_raw_event()
        self.align_old_member_status_for_raw_event()

        self.document = self.generate_event_document_model()
        # reference to EventDocument index convention: <bot.configs.name>-<bot.configs.version>-event-chatID-userID
        self.index = f'{self.document.Index.name}-{abs(self.internal_event.chat_id)}-{self.internal_event.user_id}'

    def process(self):
        """ Entrypoint to EventInterface, holding the main logic. """

        logger.info(f'[EventsDatabaseEventInterface] INDEX NAME -- {self.index} ')
        self.document.save(index=self.index)
