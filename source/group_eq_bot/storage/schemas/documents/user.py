from datetime import datetime

from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra

from elasticsearch_dsl import Document, InnerDoc, Object, Keyword, Text, Date

# Fetch bot configuration with hydra compose api
# https://hydra.cc/docs/advanced/compose_api/
initialize(version_base="1.2", config_path="../../../configurations", job_name="user_schema")
configurations = compose(config_name="configuration")
GlobalHydra.instance().clear()


class User(InnerDoc):
    user_id = Text(fields={'keyword': Keyword()}, required=True)
    first_name = Text(multi=True, fields={'keyword': Keyword()}, required=True)
    last_name = Text(multi=True, fields={'keyword': Keyword()}, required=True)
    username = Text(multi=True, fields={'keyword': Keyword()}, required=True)
    current_status = Text(fields={'keyword': Keyword()}, required=True)
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
        name = f'{configurations.events_driven_database.indices.template}-user'
        settings = {
            "number_of_shards": configurations.events_driven_database.settings.default_number_of_shards,
            "number_of_replicas": configurations.events_driven_database.settings.default_number_of_replicas
        }
