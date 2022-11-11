import datetime
from interfaces.models.internal_event.event import ExpectedInternalEvent

from elasticsearch_dsl import (
    Date,
    Document,
    Long,
    Nested,
    Object,
    Text
)


class ContentMetadata(Document):
    offset: Long(required=True)
    length: Long(required=True)
    type: Text(required=True)


class Event(Document):
    user_id: Long(required=True)
    message_id: Long(required=True)
    event_time: Date(required=True)
    event_type: Text(required=True)
    content: Text(required=True)
    content_metadata: Nested(ContentMetadata, required=True)
    raw_event: Object(ExpectedInternalEvent, required=True)


class GroupEvent(Document):
    event_id: Long(required=True)
    event: Nested(Event)
    created = Date()

    class Index:
        name = "test-qa-site"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    def save(self, ** kwargs):
        """ Override of 'Document.save()' method, which sets current date before saving document. """
        self.created = datetime.now()
        return super().save(** kwargs)


from interfaces.telegram_event_validator.validator import EventValidator
from tests.data.telegram_fake_events import fake_public_message_event, fake_public_member_event

object = EventValidator(fake_public_message_event).validated_internal_event
print(object)