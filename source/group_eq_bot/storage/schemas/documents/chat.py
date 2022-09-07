from datetime import datetime

from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra

from elasticsearch_dsl import Document, InnerDoc, Date, Keyword, Text, Long, Object

# Fetch bot configuration with hydra compose api
# https://hydra.cc/docs/advanced/compose_api/
initialize(version_base="1.2", config_path="../../../configurations", job_name="chat_schema")
configurations = compose(config_name="configuration")
GlobalHydra.instance().clear()


class Chat(InnerDoc):
    chat_id = Long(required=True)
    chat_name = Text(fields={"keyword": Keyword()}, required=True)
    chat_type = Text(fields={"keyword": Keyword()}, required=True)


class ChatDocument(Document):
    """ ChatDocument interface based on Elasticsearch-dsl document functionalities,
    which is responsible both for document and index management.

    Notes:
         index is formed as:
            convention: <bot.configs.name>-<bot.configs.version>-chats-name-id-mappings
                <bot.configs.name>-<bot.configs.version> <-- is template, stored in configs
            example: who-is-1.0-chats-name-id-mappings
    """

    chat: Object(Chat, required=True)
    created = Date()

    def save(self, ** kwargs):
        """ Override of 'Document.save()' method, which sets current date before saving document. """
        self.created = datetime.now()
        return super().save(** kwargs)

    class Index:
        name = configurations.events_driven_database.indices.template
        settings = {
            "number_of_shards": configurations.events_driven_database.settings.default_number_of_shards,
            "number_of_replicas": configurations.events_driven_database.settings.default_number_of_replicas
        }
