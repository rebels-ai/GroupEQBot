from datetime import datetime

from elasticsearch_dsl import Date, Document, Long, Nested, Object, Text, Boolean

from interfaces.models.internal_event.event import ExpectedInternalEvent
from utilities.configurations_constructor.constructor import Constructor
from storage.connectors.connector import connection


class Status(Document):
    """ Data model for user statuses data for writing to database """

    current_status = Text(required=True)
    change_history_status = Nested()


class Metadata(Document):
    """ Data model for user metadata for writing to database """

    change_history_firstname = Nested()
    change_history_lastname = Nested()
    change_history_username = Nested()


class Validation(Document):
    """ Data model for user validation for writing to database """

    passed = Boolean(required=True)
    start_time = Date()
    end_time = Date()


class Statistics(Document):
    """ Data model for user metrics for writing to database """

    total_messages_count = Long()


class Event(Document):
    """ Data model for user properties for writing to database """

    status = Object(Status)
    metadata = Object(Metadata)
    validation = Object(Validation)
    statistics = Object(Statistics)


class GroupUser(Document):
    """ Data model for user document for writing to database """

    user_id = Long(required=True)
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
    """ Interface for building document for GroupUser index based on 
        Status, Validation, Metadata, Event and GroupUser data models """

    def __init__(self, object: ExpectedInternalEvent):
        self.object = object
        self.status = None
        self.validation = None
        self.metadata = None
        self.event = None
        self.schema = None
        self.index_name = None

    def build_status_data(self):
        """ Method, which builds Status document, based on Status data model """

        current_status = self.object.new_status
        change_history_status = [{current_status: self.object.event_time}]
        self.status = Status(current_status=current_status, change_history_status=change_history_status)

    def build_validation(self):
        """ Method, which builds Validation document, based on Validation data model """

        self.validation = Validation(passed=False)

    def build_metadata(self):
        """ Method, which builds Metadata document, based on Metadata data model """

        event_time = self.object.event_time

        #  lastname and username can be empty, None values are not accepted in DB
        last_name = self.object.last_name
        username = self.object.username

        change_history_firstname = [{self.object.first_name: event_time}]

        if last_name and not username:
            change_history_lastname = [{self.object.last_name: event_time}]

            self.metadata = Metadata(change_history_firstname=change_history_firstname, 
                                     change_history_lastname=change_history_lastname)
        
        elif not last_name and username:
            change_history_username = [{self.object.username: event_time}]

            self.metadata = Metadata(change_history_firstname=change_history_firstname, 
                                     change_history_username=change_history_username)

        else:
            change_history_lastname = [{self.object.last_name: event_time}]
            change_history_username = [{self.object.username: event_time}]

            self.metadata = Metadata(change_history_firstname=change_history_firstname, 
                                     change_history_lastname=change_history_lastname,
                                     change_history_username=change_history_username)

    def build_event(self):
        """ Method, which builds Event document, based on Event data model """

        self.event = Event(status=self.status, validation=self.validation, metadata=self.metadata)

    def build_schema(self):
        """ Method, which builds document schema, based on GroupUser data model """

        self.schema = GroupUser(user_id=self.object.user_id, event=self.event)

    def build_index_name(self):
        """ Method, which builds index name for GroupUser index """

        self.index_name = f'{self.schema.Index.name}-group-users-{abs(self.object.chat_id)}'

    def build(self):
        """ Method, which generates the whole document ready to be saved to database  """

        self.build_status_data()
        self.build_validation()
        self.build_metadata()
        self.build_event()
        self.build_schema()
        self.build_index_name()

        return self
