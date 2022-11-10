from dataclasses import dataclass
from storage.schemas.new_schema import NewSchema
from interfaces.models.internal_event.event import ExpectedInternalEvent
from storage.connectors.connector import connection
from utilities.configurations_constructor.constructor import Constructor
CONFIGURATIONS = Constructor().configurations

@dataclass
class NewIndex(NewSchema):
    internal_event: ExpectedInternalEvent

    def align_chat_id(self):
        self.chat_id = abs(self.internal_event.chat_id)

    def __post_init__(self):
        self.align_chat_id()

    class Index:
        name = f'{CONFIGURATIONS.events_database.indices.index_template}-new-index'
        settings = {
            "number_of_shards": CONFIGURATIONS.events_database.infrastructure.number_of_shards,
            "number_of_replicas": CONFIGURATIONS.events_database.infrastructure.number_of_replicas
        }


from interfaces.telegram_event_validator.validator import EventValidator
from tests.data.telegram_fake_events import fake_public_message_event, fake_public_member_event, fake_private_message_event, fake_private_member_event

object=EventValidator(fake_private_message_event).validated_internal_event
index = NewIndex(object)
print(index)
index.save()
