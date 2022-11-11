from datetime import datetime

from elasticsearch_dsl import Date, Document, Long, Nested, Object, Text, Boolean, InnerDoc

from interfaces.models.internal_event.event import ExpectedInternalEvent
from storage.connectors.connector import connection
from utilities.configurations_constructor.constructor import Constructor
CONFIGURATIONS = Constructor().configurations


class Status(Document):
    current_status = Text(required=True)
    change_history_status = Nested()


class Metadata(Document):
    change_history_firstname = Nested()
    change_history_lastname = Nested()
    change_history_username = Nested()


class Validation(Document):
    passed = Boolean(required=True)
    start_time = Date()
    end_time = Date()


class Statistics(Document):
    total_messages_count = Long()


class Event(Document):
    status = Object(Status)
    metadata = Object(Metadata)
    validation = Object(Validation)
    statistics = Object(Statistics)


class GroupUser(Document):
    user_id = Long(required=True)
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
        self.status = None
        self.validation = None
        self.event = None
        self.schema = None
        self.index_name = None

    def build_status_data(self):
        self.status = Status(current_status=self.object.new_status)

    def build_validation(self):
        self.validation = Validation(passed=False)

    def build_event(self):
        self.event = Event(status=self.status, validation=self.validation)

    def build_schema(self):
        self.schema = GroupUser(user_id=self.object.user_id,
                                event=self.event)

    def build_index_name(self):
        self.index_name = f'{self.schema.Index.name}-group-users-{abs(self.object.chat_id)}'

    def build(self):
        self.build_status_data()
        self.build_validation()
        self.build_event()
        self.build_schema()
        self.build_index_name()

        return self
