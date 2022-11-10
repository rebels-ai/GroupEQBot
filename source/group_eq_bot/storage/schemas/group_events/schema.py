from datetime import datetime

import shortuuid
from elasticsearch_dsl import Date, Document, Long, Nested, Object, Text

from interfaces.models.internal_event.event import ExpectedInternalEvent
from storage.connectors.connector import connection
from utilities.configurations_constructor.constructor import Constructor
CONFIGURATIONS = Constructor().configurations


class Event(Document):
    user_id: Long(required=True)
    message_id: Long(required=True)
    event_time: Date(required=True)
    event_type: Text(required=True)
    content: Text(required=True)
    raw_event: Object(required=True)


class GroupEvent(Document):
    event_id: Long(required=True)
    event: Nested(Event, required=True)
    created = Date()

    class Index:
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
    def __init__(self, object: ExpectedInternalEvent):
        self.object = object
        self.event_id = self.generate_event_id()
        self.event = None
        self.schema = None
        self.index_name = None

    @staticmethod
    def generate_event_id() -> int:
        # @TODO: change back to uuid
        shortuuid.set_alphabet('0123456789')
        return int(shortuuid.random(length=16))

    def build_event(self):
        self.event = Event(user_id=self.object.user_id,
                           message_id=self.object.message_id,
                           event_time=self.object.event_time,
                           event_type=self.object.event_type,
                           content=self.object.message,
                           raw_event=self.object.dict())

    def build_schema(self):
        self.schema = GroupEvent(event_id=self.event_id,
                                 event=self.event)

    def build_index_name(self):
        self.index_name = f'{self.schema.Index.name}-GroupEvents-{abs(self.object.chat_id)}'

    def build(self):
        self.build_event()
        self.build_schema()
        self.build_index_name()
        return self
