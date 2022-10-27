from enum import Enum


class ChatType(Enum):
    """ Internal wrapper on ChatType of telegram Update (TelegramEvent) definition used in ExpectedInternalEvent. 

        Notes: 
            - Telegram supports 4 ChatTypes (PRIVATE, GROUP, SUPERGROUP or CHANNEL)
            - GroupEQBot supports 3 ChatTypes (PRIVATE, GROUP, SUPERGROUP)
              * PRIVATE    - 1:1    user - bot 
              * GROUP      - 1:many user - users  (group size <= 200 members)
              * SUPERGROUP - 1:many user - users  (group size > 200 members)
    """

    private = 'private'
    public = ['supergroup', 'group']
