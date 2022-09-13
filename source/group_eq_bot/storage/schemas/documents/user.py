from datetime import datetime
from elasticsearch_dsl import Document, InnerDoc, Object, Keyword, Text, Date

from utilities.configurations_constructor.constructor import Constructor
CONFIGURATIONS = Constructor().configurations


class User(InnerDoc):
    user_id = Text(fields={'keyword': Keyword()}, required=True)
    first_name = Text(multi=True, fields={'keyword': Keyword()}, required=True)
    last_name = Text(multi=True, fields={'keyword': Keyword()})
    username = Text(multi=True, fields={'keyword': Keyword()})
    last_activity = Date(required=True)


class UserDocument(Document):
    """ UserDocument interface based on Elasticsearch-dsl document functionalities,
    which is responsible both for document and index management.

    Notes:
         index is formed as:
            convention: <bot.configs.name>-<bot.configs.version>-user-chatID-userID
                <bot.configs.name>-<bot.configs.version> <-- is template, stored in configs
            example: who-is-1.0-user-1234567-9876518
    """

    user = Object(User, required=True)
    created = Date()

    def save(self, **kwargs):
        """ Override of 'Document.save()' method, which sets current date before saving document. """
        self.created = datetime.now()
        return super().save(**kwargs)

    class Index:
        name = f'{CONFIGURATIONS.events_database.indices.index_template}-user'
        settings = {
            "number_of_shards": CONFIGURATIONS.events_database.infrastructure.number_of_shards,
            "number_of_replicas": CONFIGURATIONS.events_database.infrastructure.number_of_replicas
        }
