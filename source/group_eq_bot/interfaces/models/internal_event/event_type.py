from enum import Enum


class EventType(Enum):
    """ Internal wrapper on EventType of telegram Update (TelegramEvent) definition used in ExpectedInternalEvent. 
    
    @TODO: re-write the description
    Notes:
        message: message will be registered from ChatType.private, ChatType.group, ChatType.supergroup
            BUT:
                ChatType.group, ChatType.supergroup events will be ingested into DB
                ChatType.private will not be ingested into DB
    """

    message = 'message'    
    member = 'chat_member'  
    bot = 'my_chat_member'
