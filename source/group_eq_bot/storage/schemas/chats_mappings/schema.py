from datetime import datetime

from elasticsearch_dsl import Date, Document, Long, Text, Nested
from interfaces.models.internal_event.event import ExpectedInternalEvent

from utilities.configurations_constructor.constructor import Constructor

from storage.connectors.connector import connection


class Event(Document):
    chat_id = Long(required=True)
    chat_name = Text(required=True, multi=True)
    chat_type = Text(required=True)


class ChatsMappings(Document):
    event = Nested(Event, multi=True)
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
    def __init__(self, object: ExpectedInternalEvent):
        self.object = object
        self.event = None
        self.schema = None
        self.index_name = None

    def build_event(self):
        chat_id = abs(self.object.chat_id)
        self.event = Event(
            chat_id=chat_id, chat_name=self.object.chat_name, chat_type=self.object.chat_name
        )

    def build_schema(self):
        self.schema = ChatsMappings(event=self.event)

    def build_index_name(self):
        self.index_name = f'{self.schema.Index.name}-chats-name-id-mappings'

    def build(self):
        self.build_event()
        self.build_schema()
        self.build_index_name()

        return self

