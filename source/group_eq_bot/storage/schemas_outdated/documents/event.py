from datetime import datetime

from storage.schemas.documents.chat import Chat
from storage.schemas.documents.user import User
from elasticsearch_dsl import Document, InnerDoc, Date, Keyword, Text, Object

from utilities.configurations_constructor.constructor import Constructor
CONFIGURATIONS = Constructor().configurations


class EventMetadata(InnerDoc):
    event_type = Text(fields={"keyword": Keyword()}, required=True)
    event_time = Date()


class Event(InnerDoc):
    raw_event = Object()
    event_metadata = EventMetadata()
    chat_metadata = Chat()
    user_metadata = User()
    message_id = Text(fields={'keyword': Keyword()})
    content = Text(fields={"keyword": Keyword()})


class EventDocument(Document):
    """ EventDocument interface based on Elasticsearch-dsl document functionalities,
    which is responsible both for document and index management.

    Notes:
         index is formed as:
            convention: c
                <bot.configs.name>-<bot.configs.version> <-- is template, stored in configs
            example: who-is-1.0-event-9876518-1234567
    """

    event = Object(Event, required=True)
    created = Date()

    def save(self, ** kwargs):
        """ Override of 'Document.save()' method, which sets current date before saving document. """
        self.created = datetime.now()
        return super().save(** kwargs)

    class Index:
        name = f'{CONFIGURATIONS.events_database.indices.index_template}-event'
        settings = {
            "number_of_shards": CONFIGURATIONS.events_database.infrastructure.number_of_shards,
            "number_of_replicas": CONFIGURATIONS.events_database.infrastructure.number_of_replicas
        }
