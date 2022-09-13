from datetime import datetime
from elasticsearch_dsl import Document, InnerDoc, Date, Keyword, Text, Long, Object


class Chat(InnerDoc):
    chat_id = Long(required=True)
    chat_name = Text(multi=True, fields={"keyword": Keyword()}, required=True)
    chat_type = Text(multi=True, fields={"keyword": Keyword()}, required=True)

    # list of user_id -- originally user_id is int type
    chat_historic_members = Text(multi=True, fields={"keyword": Keyword()}, required=True)


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
