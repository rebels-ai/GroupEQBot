from datetime import datetime

from elasticsearch_dsl import Date, Document, Long, Text

from interfaces.models.internal_event.event import ExpectedInternalEvent
from utilities.configurations_constructor.constructor import Constructor
from storage.connectors.connector import connection


class ChatsMapping(Document):
    """ Data model for chats id and names mappings for writing to database """

    chat_id = Long(required=True)
    chat_name = Text(required=True, multi=True)
    chat_type = Text(required=True)
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
    """ Interface for building document for ChatsMapping index based on 
        ChatsMapping data model """

    def __init__(self, object: ExpectedInternalEvent):
        self.object = object
        self.schema = None
        self.index_name = None

    def build_schema(self):
        """ Method, which builds document schema, based on BotEvent data model """

        chat_id = abs(self.object.chat_id)
        self.schema = ChatsMapping(chat_id=chat_id, chat_name=self.object.chat_name, chat_type=self.object.chat_type)

    def build_index_name(self):
        """ Method, which builds index name for BotEvent index """

        self.index_name = f'{self.schema.Index.name}-chats-name-id-mappings'

    def build(self):
        """ Method, which generates the whole document ready to be saved to database  """

        self.build_schema()
        self.build_index_name()

        return self

