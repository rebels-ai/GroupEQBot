import shortuuid
from datetime import datetime

from elasticsearch_dsl import Date, Document, Long, Nested, Object, Text

from interfaces.models.internal_event.event import ExpectedInternalEvent
from utilities.configurations_constructor.constructor import Constructor
from storage.connectors.connector import connection


class Event(Document):
    """ Data model for event for writing to database """

    user_id = Long(required=True)
    message_id = Long()
    event_time = Date(required=True)
    event_type = Text(required=True)
    content = Text()
    raw_event = Object(required=True)


class GroupEvent(Document):
    """ Data model for group event for writing to database """

    event_id = Long(required=True)
    event = Nested(Event, required=True)
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
    """ Interface for building document for GroupEvent index based on 
        Event and GroupEvent data models """

    def __init__(self, object: ExpectedInternalEvent):
        self.object = object
        self.event_id = self.generate_event_id()
        self.event = None
        self.schema = None
        self.index_name = None

    @staticmethod
    def generate_event_id() -> int:
        """ Method, which generates id for event for writing in database

            Notes: @TODO: change back to uuid + botEvent eventID is generated same way
        """

        shortuuid.set_alphabet('0123456789')
        event_id = int(shortuuid.random(length=16))

        return event_id

    def build_event(self):
        """ Method, which builds Event document, based on Event data model """

        self.event = Event(user_id=self.object.user_id,
                           message_id=self.object.message_id,
                           event_time=self.object.event_time,
                           event_type=self.object.event_type,
                           content=self.object.message,
                           raw_event=self.object.dict())

    def build_schema(self):
        """ Method, which builds document schema, based on GroupEvent data model """

        self.schema = GroupEvent(event_id=self.event_id,
                                 event=self.event)

    def build_index_name(self):
        """ Method, which builds index name for GroupEvent index """

        self.index_name = f'{self.schema.Index.name}-group-events-{abs(self.object.chat_id)}'

    def build(self):
        """ Method, which generates the whole document ready to be saved to database  """

        self.build_event()
        self.build_schema()
        self.build_index_name()

        return self
