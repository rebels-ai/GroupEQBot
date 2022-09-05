from telegram.constants import ChatMemberStatus, ChatType
from telegram import Update as TelegramEvent


"""
    Short description of values for fake Message | Member events

    | Chat type |  Event type  | Chat ID | User ID | Message ID |              Chat name             |                 User first name               |                  User last name              |            Username           | User new status | User old status |    Message text   |  Event time
     public     chat_member     -111111   1111      None         test-public-member-event-chat-name   public-member-event-new-chat-member-first-name  public-member-event-new-chat-member-last-name  None                            member            banned            None                1661166376
     public     message         -222222   2222      22           test-public-message-event-chat-name  public-message-event-first-name                 public-message-event-last-name                 public-message-event-username   None              None              public-chat-text    1661166289
     private    message          333333   3333      33           who-is-bot-private-chat              private-message-event-first-name                private-message-event-last-name                private-message-event-username  None              None              private-chat-text   1661172025
     private    my_chat_member   444444   4444      None         who-is-bot-private-chat              bot-first-name                                  None                                           bot-username                    member            banned            None                1661172863

"""


member_event_json_public = {
    "update_id": 801018037,
    "chat_member": {
        "chat": {
            "id": -111111,
            "type": ChatType.SUPERGROUP,
            "username": "test-public-member-event-chat-username",
            "title": "test-public-member-event-chat-name"
        },
        "date": 1661166376,
        "old_chat_member": {
            "until_date": 0,
            "user": {
                "is_bot": False,
                "first_name": "public-member-event-old-chat-member-first-name",
                "last_name": "public-member-event-old-chat-member-last-name",
                "id": 1111,
                "language_code": "en"
            },
            "status": ChatMemberStatus.BANNED
        },
        "new_chat_member": {
            "user": {
                "is_bot": False,
                "first_name": "public-member-event-new-chat-member-first-name",
                "last_name": "public-member-event-new-chat-member-last-name",
                "id": 1111,
                "language_code": "en"
            },
            "status": ChatMemberStatus.MEMBER
        },
        "from": {
            "is_bot": False,
            "username": "who-did-the-change-username",
            "first_name": "who-did-the-change-first-name",
            "last_name": "who-did-the-change-lastname",
            "id": 1010,
            "language_code": "en"
        }
    }
}

message_event_json_public = {
    "update_id": 801018035,
    "message": {
        "chat": {
            "id": -222222,
            "type": ChatType.SUPERGROUP,
            "username": "test-public-message-event-chat-username",
            "title": "test-public-message-event-chat-name"
        },
        "text": "public-chat-text",
        "group_chat_created": False,
        "entities": [],
        "new_chat_members": [],
        "new_chat_photo": [],
        "message_id": 22,
        "delete_chat_photo": False,
        "caption_entities": [],
        "date": 1661166289,
        "supergroup_chat_created": False,
        "photo": [],
        "channel_chat_created": False,
        "from": {
            "is_bot": False,
            "username": "public-message-event-username",
            "first_name": "public-message-event-first-name",
            "last_name": "public-message-event-last-name",
            "id": 2222,
            "language_code": "en"
        }
    }
}

message_event_json_private = {
    "update_id": 801018038,
    "message": {
        "chat": {
            "id": 333333,
            "type": ChatType.PRIVATE,
            "username": "private-message-event-chat-username",
            "first_name": "private-message-event-chat-first-name",
            "last_name": "private-message-event-chat-last-name",
        },
        "text": "private-chat-text",
        "group_chat_created": False,
        "entities": [],
        "new_chat_members": [],
        "new_chat_photo": [],
        "message_id": 33,
        "delete_chat_photo": False,
        "caption_entities": [],
        "date": 1661172025,
        "supergroup_chat_created": False,
        "photo": [],
        "channel_chat_created": False,
        "from": {
            "is_bot": False,
            "username": "private-message-event-username",
            "first_name": "private-message-event-first-name",
            "last_name": "private-message-event-last-name",
            "id": 3333,
            "language_code": "en"
        }
    }
}

member_event_json_private = {
    "update_id": 801018040,
    "my_chat_member": {
        "chat": {
            "id": 444444,
            "type": ChatType.PRIVATE,
            "username": "private-member-event-chat-username",
            "first_name": "private-member-event-chat-first-name",
            "last_name": "private-member-event-chat-last-name",
        },
        "date": 1661172863,
        "old_chat_member": {
            "until_date": 0,
            "user": {
                "is_bot": True,
                "username": "bot-username",
                "first_name": "bot-first-name",
                "id": 5366972505
            },
            "status": ChatMemberStatus.BANNED
        },
        "new_chat_member": {
            "user": {
                "is_bot": True,
                "username": "bot-username",
                "first_name": "bot-first-name",
                "id": 5366972505
            },
            "status": ChatMemberStatus.MEMBER
        },
        "from": {
            "is_bot": False,
            "username": "private-member-event-username",
            "first_name": "private-member-event-first-name",
            "last_name": "private-member-event-last-name",
            "id": 4444,
            "language_code": "en"
        }
    }
}


fake_public_message_event = TelegramEvent(**message_event_json_public)
fake_private_message_event = TelegramEvent(**message_event_json_private)
fake_public_member_event = TelegramEvent(**member_event_json_public)
fake_private_member_event = TelegramEvent(**member_event_json_private)
