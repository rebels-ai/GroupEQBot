"""
Folder structure:

schemas
    group_events.py
indeces
    group_events.py


schemas.group_events.py

class GroupEventsSchema:
    

    def generate_schema(self)
        self.internal_event.....


indeces.group_events.py
from schemas.group_events import GroupEventsSchema


class GroupEventsIndex(Document):
    object = Object(GroupEventSchema, required=True)
    created = Date()

    def save(self, ** kwargs):
        ''' Override of 'Document.save()' method, which sets current date before saving document. '''
        self.created = datetime.now()
        return super().save(** kwargs)

    class Index:
        name = f'{CONFIGURATIONS.events_database.indices.index_template}-event'
        settings = {
            "number_of_shards": CONFIGURATIONS.events_database.infrastructure.number_of_shards,
            "number_of_replicas": CONFIGURATIONS.events_database.infrastructure.number_of_replicas
        }

from tests.fake_data import ... externalevent

--> ExpectedInternalEvent

index = GropEventsIndex(object=ExpectedInternalEvent(...))
print(index)

index.save()

"""


from datetime import datetime

from elasticsearch_dsl import Document, Date, Object, Index

from storage.connectors.connector import connection
from storage.schemas.group_event import GroupEventsSchema
from utilities.configurations_constructor.constructor import Constructor
CONFIGURATIONS = Constructor().configurations


class GroupEventsIndex(Document):
    """ GroupEventsIndex interface based on Elasticsearch-dsl document functionalities,
    which is responsible both for document and index management.

    Notes:
         index is formed as:
            convention: <bot.configs.name>-<bot.configs.version>-group-events-chatID
                <bot.configs.name>-<bot.configs.version> <-- is template, stored in configs
            example: group_eq_bot-1.0-group-events-987651567
    """

    object = Object(GroupEventsSchema, required=True)
    created = Date()

    def save(self, ** kwargs):
        """ Override of 'Document.save()' method, which sets current date before saving document. """
        self.created = datetime.now()
        return super().save(** kwargs)

    class Index:
        name = f'{CONFIGURATIONS.events_database.indices.index_template}-group-events'
        settings = {
            "number_of_shards": CONFIGURATIONS.events_database.infrastructure.number_of_shards,
            "number_of_replicas": CONFIGURATIONS.events_database.infrastructure.number_of_replicas
        }

from interfaces.telegram_event_validator.validator import EventValidator
from tests.data.telegram_fake_events import fake_public_message_event, fake_public_member_event, fake_private_message_event, fake_private_member_event

object=EventValidator(fake_private_message_event).validated_internal_event
index = GroupEventsIndex(object=object)
index_name = f'{index.Index.name}-{abs(object.chat_id)}'
print(index)
print(index_name)
# document.save(index=index, return_doc_meta=True)
# print(document.object)
index.save(index=index_name)

# group_chat = Index(f'{CONFIGURATIONS.events_database.indices.index_template}-group-events')
# group_chat.settings(number_of_shards=CONFIGURATIONS.events_database.infrastructure.number_of_shards,
#                     number_of_replicas=CONFIGURATIONS.events_database.infrastructure.number_of_replicas)
# group_chat.document(GroupEventsIndex)
# group_chat.create()
