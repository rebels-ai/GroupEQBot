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
        shortuuid.set_alphabet('0123456789')
        return int(shortuuid.random(length=16))

    def build_event(self):
        self.event = Event(user_id=object.user_id,
                           message_id=object.message_id,
                           event_time=object.event_time,
                           event_type=object.event_type,
                           content=object.message,
                           raw_event=object.dict())

    def build_schema(self):
        self.schema = GroupEvent(event_id=self.event_id,
                                 event=self.event)

    def build_index_name(self):
        self.index_name = f'{self.schema.Index.name}-group-events-{abs(self.object.chat_id)}'

    def build(self):
        self.build_event()
        self.build_schema()
        self.build_index_name()
        return self


from interfaces.telegram_event_validator.validator import EventValidator
from tests.data.telegram_fake_events import fake_public_message_event, fake_public_member_event, fake_private_member_event, fake_private_message_event

object = EventValidator(fake_public_message_event).validated_internal_event


document = Builder(object=object).build()

print(document.schema.save(index=document.index_name))
