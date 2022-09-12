from datetime import datetime

from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra

from elasticsearch_dsl import Document, InnerDoc, Date, Keyword, Text, Object
from storage.schemas.documents.chat import Chat
from storage.schemas.documents.user import User


# Fetch bot configuration with hydra compose api
# https://hydra.cc/docs/advanced/compose_api/
initialize(version_base="1.2", config_path="../../../configurations", job_name="event_schema")
configurations = compose(config_name="configuration")
GlobalHydra.instance().clear()


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
        name = f'{configurations.events_driven_database.indices.template}-event'
        settings = {
            "number_of_shards": configurations.events_driven_database.settings.default_number_of_shards,
            "number_of_replicas": configurations.events_driven_database.settings.default_number_of_replicas
        }
