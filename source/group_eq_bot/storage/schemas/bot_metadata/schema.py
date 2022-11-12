from datetime import datetime

from elasticsearch_dsl import Date, Document, Long, Object, Text

from interfaces.models.internal_event.event import ExpectedInternalEvent
from utilities.configurations_constructor.constructor import Constructor

from storage.connectors.connector import connection


class Event(Document):
    user_id_added_bot = Text(required=True)
    chat_name = Text(required=True)
    chat_type = Text(required=True)
    bot_add_time = Date(required=True)
    bot_status = Text(required=True)


class BotMetadata(Document):
    chat_id = Long(required=True)
    event = Object(Event, required=True)
    created = Date()

    class Index:
        CONFIGURATIONS = Constructor ().configurations

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
        self.event = Event(
            user_id_added_bot=self.object.event.my_chat_member.from_user.id, chat_name=self.object.chat_name,
            chat_type=self.object.chat_type, bot_add_time=self.object.event_time, bot_status=self.object.new_status
        )

    def build_schema(self):
        chat_id = abs(self.object.chat_id)
        self.schema = BotMetadata(chat_id=chat_id, event=self.event)

    def build_index_name(self):
        self.index_name = f'{self.schema.Index.name}-bot-metadata'

    def build(self):
        self.build_event()
        self.build_schema()
        self.build_index_name()

        return self
