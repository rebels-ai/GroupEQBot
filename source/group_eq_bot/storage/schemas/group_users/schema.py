from datetime import datetime

import shortuuid
from elasticsearch_dsl import Date, Document, Long, Nested, Object, Text, Boolean

from interfaces.models.internal_event.event import ExpectedInternalEvent
from storage.connectors.connector import connection
from utilities.configurations_constructor.constructor import Constructor
CONFIGURATIONS = Constructor().configurations


class Status(Document):
    currnet_status = Text()
    change_history_status = Object()

class FirstName(Document):
    firstname = Text(multi=True, required=True)
    timestamp = Date()

class LastName(Document):
    lastname = Text(multi=True, required=True)
    timestamp = Date()

class Username(Document):
    username = Text(multi=True, required=True)
    timestamp = Date()

class Metadata(Document):
    change_history_firstname = Object()
    change_history_lastname = Object()
    change_history_username = Object()


class Validation(Document):
    passed = Boolean(required=True)
    start_time = Date()
    end_time = Date()


class User(Document):
    user_id = Long(required=True)
    status = Nested(Status, required=True)
    metadata = Nested(Metadata, required=True)
    validation = Nested(Validation, required=True)
