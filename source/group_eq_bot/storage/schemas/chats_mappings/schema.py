from datetime import datetime

from elasticsearch_dsl import Date, Document, Long, Text

from interfaces.models.internal_event.event import ExpectedInternalEvent
from storage.connectors.connector import connection
from utilities.configurations_constructor.constructor import Constructor
CONFIGURATIONS = Constructor().configurations


class Chat(Document):
    chat_id = Long(required=True, )
    chat_name = Text(required=True, multi=True)
    chat_type = Text(required=True)
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
        self.schema = None
        self.index_name = None

    def build_schema(self):
        self.schema = Chat(chat_id=abs(self.object.chat_id),
                           chat_name=self.object.chat_name)

    def build_index_name(self):
        self.index_name = f'{self.schema.Index.name}-chats-name-id-mappings'

    def build(self):
        self.build_schema()
        self.build_index_name()
        return self

from interfaces.telegram_event_validator.validator import EventValidator
from tests.data.telegram_fake_events import fake_public_message_event, fake_public_member_event, fake_private_member_event, fake_private_message_event

object = EventValidator(fake_public_message_event).validated_internal_event

document = Builder(object=object).build()

print(document.schema.save(index=document.index_name))
