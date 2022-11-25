import shortuuid
from datetime import datetime

from elasticsearch_dsl import Date, Document, Long, Object, Text

from interfaces.models.internal_event.event import ExpectedInternalEvent
from utilities.configurations_constructor.constructor import Constructor
from storage.connectors.connector import connection


class Message(Document):
    """ Data model for user message for writing to database """

    message_id = Long()
    event_time = Date(required=True)
    content = Text(required=True)
    raw_event = Object(required=True)


class UserEvent(Document):
    """ Data model for user event for writing to database """

    event_id = Long(required=True)
    message = Object(Message, required=True)


class Event(Document):
    """ Data model for user for writing to database """

    user_id = Long(required=True)
    user_event = Object(UserEvent, required=True, multi=True)


class BotEvent(Document):
    """ Data model for private bot event for writing to database """

    chat_id = Long(required=True)
    event = Object(Event, required=True, multi=True)
    created = Date()

    class Index:
        CONFIGURATIONS = Constructor().configurations

        name = f"{CONFIGURATIONS.events_database.indices.index_template}"
        settings = {
            "number_of_shards": CONFIGURATIONS.events_database.infrastructure.number_of_shards,
            "number_of_replicas": CONFIGURATIONS.events_database.infrastructure.number_of_replicas
        }

    def save(self, ** kwargs):
        """ Override of 'Document.save()' method, which sets current date before saving document. """
        self.created = datetime.now()
        return super().save(** kwargs)


class Builder:
    """ Interface for building document for BotEvent index based on 
        Message, UserEvent, Event and BotEvent data models """

    def __init__(self, object: ExpectedInternalEvent, chat_id: int):
        self.object = object
        self.event_id = self.generate_event_id()
        self.message = None
        self.user_event = None
        self.event = None
        self.schema = None
        self.index_name = None
        self.chat_id = chat_id

    @staticmethod
    def generate_event_id() -> int:
        """ Method, which generates id for event for writing in database

            Notes: @TODO: change back to uuid + groupEvent eventID is generated same way
        """

        shortuuid.set_alphabet('0123456789')
        event_id = int(shortuuid.random(length=16))

        return event_id

    def build_message(self):
        """ Method, which builds Message document, based on Message data model """

        self.message = Message(
            message_id=self.object.message_id, event_time=self.object.event_time,
            content=self.object.message, raw_event=self.object.dict()
        )

    def build_user_event(self):
        """ Method, which builds UserEvent document, based on UserEvent data model """

        self.user_event = UserEvent(event_id=self.event_id, message=self.message)

    def build_event(self):
        """ Method, which builds Event document, based on Event data model """

        self.event = Event(user_id=self.object.user_id, user_event=self.user_event)

    def build_schema(self):
        """ Method, which builds document schema, based on BotEvent data model """

        chat_id = self.chat_id
        self.schema = BotEvent(chat_id=chat_id, event=self.event)

    def build_index_name(self):
        """ Method, which builds index name for BotEvent index """

        self.index_name = f'{self.schema.Index.name}-bot-events'

    def build(self):
        """ Method, which generates the whole document ready to be saved to database  """

        self.build_message()
        self.build_user_event()
        self.build_event()
        self.build_schema()
        self.build_index_name()

        return self
