from unittest import TestCase

from group_eq_bot.interfaces.telegram_event_router import EventValidator
from group_eq_bot.tests.data.telegram_fake_events import fake_public_member_event, fake_public_message_event, fake_private_message_event


class TestRouterEventValidator(TestCase):

    PUBLIC_MEMBER_EVENT_CHAT_TYPE = "supergroup"
    PUBLIC_MESSAGE_EVENT_CHAT_TYPE = "supergroup"
    PRIVATE_MESSAGE_EVENT_CHAT_TYPE = "private"

    PUBLIC_MEMBER_EVENT_TYPE = "chat_member"
    PUBLIC_MESSAGE_EVENT_TYPE = "message"
    PRIVATE_MESSAGE_EVENT_TYPE = "message"

    PUBLIC_MEMBER_EVENT_CHAT_NAME = "test-public-member-event-chat-name"
    PUBLIC_MESSAGE_EVENT_CHAT_NAME = "test-public-message-event-chat-name"
    PRIVATE_MESSAGE_EVENT_CHAT_NAME = "who-is-bot-private-chat"

    PUBLIC_MEMBER_EVENT_CHAT_ID = -111111
    PUBLIC_MESSAGE_EVENT_CHAT_ID = -222222
    PRIVATE_MESSAGE_EVENT_CHAT_ID = 333333

    PUBLIC_MEMBER_EVENT_USER_ID = 1111
    PUBLIC_MESSAGE_EVENT_USER_ID = 2222
    PRIVATE_MESSAGE_EVENT_USER_ID = 3333

    PUBLIC_MEMBER_EVENT_MESSAGE_ID = None
    PUBLIC_MESSAGE_EVENT_MESSAGE_ID = 22
    PRIVATE_MESSAGE_EVENT_MESSAGE_ID = 33

    PUBLIC_MEMBER_EVENT_USER_FIRST_NAME = "public-member-event-new-chat-member-first-name"
    PUBLIC_MESSAGE_EVENT_USER_FIRST_NAME = "public-message-event-first-name"
    PRIVATE_MESSAGE_EVENT_USER_FIRST_NAME = "private-message-event-first-name"

    PUBLIC_MEMBER_EVENT_USER_LAST_NAME = "public-member-event-new-chat-member-last-name"
    PUBLIC_MESSAGE_EVENT_USER_LAST_NAME = "public-message-event-last-name"
    PRIVATE_MESSAGE_EVENT_USER_LAST_NAME = "private-message-event-last-name"

    PUBLIC_MEMBER_EVENT_USERNAME = None
    PUBLIC_MESSAGE_EVENT_USERNAME = "public-message-event-username"
    PRIVATE_MESSAGE_EVENT_USERNAME = "private-message-event-username"

    PUBLIC_MEMBER_EVENT_USER_NEW_STATUS = "member"
    PUBLIC_MESSAGE_EVENT_USER_NEW_STATUS = None
    PRIVATE_MESSAGE_EVENT_USER_NEW_STATUS = None

    PUBLIC_MEMBER_EVENT_USER_OLD_STATUS = "kicked"
    PUBLIC_MESSAGE_EVENT_USER_OLD_STATUS = None
    PRIVATE_MESSAGE_EVENT_USER_OLD_STATUS = None

    PUBLIC_MEMBER_EVENT_TIME = 1661166376.0
    PUBLIC_MESSAGE_EVENT_TIME = 1661166289.0
    PRIVATE_MESSAGE_EVENT_TIME = 1661172025.0

    PUBLIC_MEMBER_EVENT_MESSAGE_TEXT = None
    PUBLIC_MESSAGE_EVENT_MESSAGE_TEXT = "public-chat-text"
    PRIVATE_MESSAGE_EVENT_MESSAGE_TEXT = "private-chat-text"


    def setUp(self):
        self.PublicMemberEventValidator = EventValidator(external_event=fake_public_member_event)
        self.PublicMessageEventValidator = EventValidator(external_event=fake_public_message_event)
        self.PrivateMessageEventValidator = EventValidator(external_event=fake_private_message_event)

    def test_get_chat_type(self):
        """ Method for testing EventValidator.get_chat_type """

        expected_public_member_event_chat_type = self.PUBLIC_MEMBER_EVENT_CHAT_TYPE
        expected_public_message_event_chat_type = self.PUBLIC_MESSAGE_EVENT_CHAT_TYPE
        expected_private_message_event_chat_type = self.PRIVATE_MESSAGE_EVENT_CHAT_TYPE

        obtained_public_member_event_chat_type = self.PublicMemberEventValidator.validated_internal_event.chat_type.value
        obtained_public_message_event_chat_type = self.PublicMessageEventValidator.validated_internal_event.chat_type.value
        obtained_private_message_event_chat_type = self.PrivateMessageEventValidator.validated_internal_event.chat_type.value

        self.assertEqual(expected_public_member_event_chat_type, obtained_public_member_event_chat_type)
        self.assertEqual(expected_public_message_event_chat_type, obtained_public_message_event_chat_type)
        self.assertEqual(expected_private_message_event_chat_type, obtained_private_message_event_chat_type)

    def test_get_event_type(self):
        """ Method for testing EventValidator.get_event_type """

        expected_public_member_event_type = self.PUBLIC_MEMBER_EVENT_TYPE
        expected_public_message_event_type = self.PUBLIC_MESSAGE_EVENT_TYPE
        expected_private_message_event_type = self.PRIVATE_MESSAGE_EVENT_TYPE

        obtained_public_member_event_type = self.PublicMemberEventValidator.validated_internal_event.event_type.value
        obtained_public_message_event_type = self.PublicMessageEventValidator.validated_internal_event.event_type.value
        obtained_private_message_event_type = self.PrivateMessageEventValidator.validated_internal_event.event_type.value

        self.assertEqual(expected_public_member_event_type, obtained_public_member_event_type)
        self.assertEqual(expected_public_message_event_type, obtained_public_message_event_type)
        self.assertEqual(expected_private_message_event_type, obtained_private_message_event_type)

    def test_get_chat_name(self):
        """ Method for testing EventValidator.get_chat_name """

        expected_public_member_event_chat_name = self.PUBLIC_MEMBER_EVENT_CHAT_NAME
        expected_public_message_event_chat_name = self.PUBLIC_MESSAGE_EVENT_CHAT_NAME
        expected_private_message_event_chat_name = self.PRIVATE_MESSAGE_EVENT_CHAT_NAME

        obtained_public_member_event_chat_name = self.PublicMemberEventValidator.validated_internal_event.chat_name
        obtained_public_message_event_chat_name = self.PublicMessageEventValidator.validated_internal_event.chat_name
        obtained_private_message_event_chat_name = self.PrivateMessageEventValidator.validated_internal_event.chat_name

        self.assertEqual(expected_public_member_event_chat_name, obtained_public_member_event_chat_name)
        self.assertEqual(expected_public_message_event_chat_name, obtained_public_message_event_chat_name)
        self.assertEqual(expected_private_message_event_chat_name, obtained_private_message_event_chat_name)

    def test_get_chat_id(self):
        """ Method for testing EventValidator.get_chat_id """

        expected_public_member_event_chat_id = self.PUBLIC_MEMBER_EVENT_CHAT_ID
        expected_public_message_event_chat_id = self.PUBLIC_MESSAGE_EVENT_CHAT_ID
        expected_private_message_event_chat_id = self.PRIVATE_MESSAGE_EVENT_CHAT_ID

        obtained_public_member_event_chat_id = self.PublicMemberEventValidator.validated_internal_event.chat_id
        obtained_public_message_event_chat_id = self.PublicMessageEventValidator.validated_internal_event.chat_id
        obtained_private_message_event_chat_id = self.PrivateMessageEventValidator.validated_internal_event.chat_id

        self.assertEqual(expected_public_member_event_chat_id, obtained_public_member_event_chat_id)
        self.assertEqual(expected_public_message_event_chat_id, obtained_public_message_event_chat_id)
        self.assertEqual(expected_private_message_event_chat_id, obtained_private_message_event_chat_id)

    def test_get_user_id(self):
        """ Method for testing EventValidator.get_user_id """

        expected_public_member_event_user_id = self.PUBLIC_MEMBER_EVENT_USER_ID
        expected_public_message_event_user_id = self.PUBLIC_MESSAGE_EVENT_USER_ID
        expected_private_message_event_user_id = self.PRIVATE_MESSAGE_EVENT_USER_ID

        obtained_public_member_event_user_id = self.PublicMemberEventValidator.validated_internal_event.user_id
        obtained_public_private_message_event_user_id = self.PublicMessageEventValidator.validated_internal_event.user_id
        obtained_private_message_event_user_id = self.PrivateMessageEventValidator.validated_internal_event.user_id

        self.assertEqual(expected_public_member_event_user_id, obtained_public_member_event_user_id)
        self.assertEqual(expected_public_message_event_user_id, obtained_public_private_message_event_user_id)
        self.assertEqual(expected_private_message_event_user_id, obtained_private_message_event_user_id)

    def test_get_message_id(self):
        """ Method for testing EventValidator.get_message_id """

        expected_public_member_event_message_id = self.PUBLIC_MEMBER_EVENT_MESSAGE_ID
        expected_public_message_event_message_id = self.PUBLIC_MESSAGE_EVENT_MESSAGE_ID
        expected_private_message_event_message_id = self.PRIVATE_MESSAGE_EVENT_MESSAGE_ID

        obtained_public_member_event_message_id = self.PublicMemberEventValidator.validated_internal_event.message_id
        obtained_public_message_event_message_id = self.PublicMessageEventValidator.validated_internal_event.message_id
        obtained_private_message_event_message_id = self.PrivateMessageEventValidator.validated_internal_event.message_id

        self.assertEqual(expected_public_member_event_message_id, obtained_public_member_event_message_id)
        self.assertEqual(expected_public_message_event_message_id, obtained_public_message_event_message_id)
        self.assertEqual(expected_private_message_event_message_id, obtained_private_message_event_message_id)

    def test_get_user_first_name(self):
        """ Method for testing EventValidator.get_user_first_name """

        expected_public_member_event_first_name = self.PUBLIC_MEMBER_EVENT_USER_FIRST_NAME
        expected_public_message_event_first_name = self.PUBLIC_MESSAGE_EVENT_USER_FIRST_NAME
        expected_private_message_event_first_name = self.PRIVATE_MESSAGE_EVENT_USER_FIRST_NAME

        obtained_public_member_event_first_name = self.PublicMemberEventValidator.validated_internal_event.first_name
        obtained_public_message_event_first_name = self.PublicMessageEventValidator.validated_internal_event.first_name
        obtained_private_message_event_first_name = self.PrivateMessageEventValidator.validated_internal_event.first_name

        self.assertEqual(expected_public_member_event_first_name, obtained_public_member_event_first_name)
        self.assertEqual(expected_public_message_event_first_name, obtained_public_message_event_first_name)
        self.assertEqual(expected_private_message_event_first_name, obtained_private_message_event_first_name)

    def test_get_user_last_name(self):
        """ Method for testing EventValidator.get_user_last_name """

        expected_public_member_event_last_name = self.PUBLIC_MEMBER_EVENT_USER_LAST_NAME
        expected_public_message_event_last_name = self.PUBLIC_MESSAGE_EVENT_USER_LAST_NAME
        expected_private_message_event_last_name = self.PRIVATE_MESSAGE_EVENT_USER_LAST_NAME

        obtained_public_member_event_last_name = self.PublicMemberEventValidator.validated_internal_event.last_name
        obtained_public_message_event_last_name = self.PublicMessageEventValidator.validated_internal_event.last_name
        obtained_private_message_event_last_name = self.PrivateMessageEventValidator.validated_internal_event.last_name

        self.assertEqual(expected_public_member_event_last_name, obtained_public_member_event_last_name)
        self.assertEqual(expected_public_message_event_last_name, obtained_public_message_event_last_name)
        self.assertEqual(expected_private_message_event_last_name, obtained_private_message_event_last_name)

    def test_get_username(self):
        """ Method for testing EventValidator.get_username """

        expected_public_member_event_username = self.PUBLIC_MEMBER_EVENT_USERNAME
        expected_public_message_event_username = self.PUBLIC_MESSAGE_EVENT_USERNAME
        expected_private_message_event_username = self.PRIVATE_MESSAGE_EVENT_USERNAME

        obtained_public_member_event_username = self.PublicMemberEventValidator.validated_internal_event.username
        obtained_public_message_event_username = self.PublicMessageEventValidator.validated_internal_event.username
        obtained_private_message_event_username = self.PrivateMessageEventValidator.validated_internal_event.username

        self.assertEqual(expected_public_member_event_username, obtained_public_member_event_username)
        self.assertEqual(expected_public_message_event_username, obtained_public_message_event_username)
        self.assertEqual(expected_private_message_event_username, obtained_private_message_event_username)

    def test_get_user_new_status(self):
        """ Method for testing EventValidator.get_user_new_status """

        expected_public_member_event_user_status = self.PUBLIC_MEMBER_EVENT_USER_NEW_STATUS
        expected_public_message_event_user_status = self.PUBLIC_MESSAGE_EVENT_USER_NEW_STATUS
        expected_private_message_event_user_status = self.PRIVATE_MESSAGE_EVENT_USER_NEW_STATUS

        obtained_public_member_event_user_status = self.PublicMemberEventValidator.validated_internal_event.new_status.value
        obtained_public_message_event_user_status = self.PublicMessageEventValidator.validated_internal_event.new_status.value
        obtained_private_message_event_user_status = self.PrivateMessageEventValidator.validated_internal_event.new_status.value

        self.assertEqual(expected_public_member_event_user_status, obtained_public_member_event_user_status)
        self.assertEqual(expected_public_message_event_user_status, obtained_public_message_event_user_status)
        self.assertEqual(expected_private_message_event_user_status, obtained_private_message_event_user_status)

    def test_get_user_old_status(self):
        """ Method for testing EventValidator.get_user_old_status """

        expected_public_member_event_user_status = self.PUBLIC_MEMBER_EVENT_USER_OLD_STATUS
        expected_public_message_event_user_status = self.PUBLIC_MESSAGE_EVENT_USER_OLD_STATUS
        expected_private_message_event_user_status = self.PRIVATE_MESSAGE_EVENT_USER_OLD_STATUS

        obtained_public_member_event_user_status = self.PublicMemberEventValidator.validated_internal_event.old_status.value
        obtained_public_message_event_user_status = self.PublicMessageEventValidator.validated_internal_event.old_status.value
        obtained_private_message_event_user_status = self.PrivateMessageEventValidator.validated_internal_event.old_status.value

        self.assertEqual(expected_public_member_event_user_status, obtained_public_member_event_user_status)
        self.assertEqual(expected_public_message_event_user_status, obtained_public_message_event_user_status)
        self.assertEqual(expected_private_message_event_user_status, obtained_private_message_event_user_status)

    def test_get_event_time(self):
        """ Method for testing EventValidator.get_event_time """

        expected_public_member_event_time = self.PUBLIC_MEMBER_EVENT_TIME
        expected_public_message_event_time = self.PUBLIC_MESSAGE_EVENT_TIME
        expected_private_message_event_time = self.PRIVATE_MESSAGE_EVENT_TIME

        obtained_public_member_event_time = self.PublicMemberEventValidator.validated_internal_event.event_time
        obtained_public_message_event_time = self.PublicMessageEventValidator.validated_internal_event.event_time
        obtained_private_message_event_time = self.PrivateMessageEventValidator.validated_internal_event.event_time

        self.assertEqual(expected_public_member_event_time, obtained_public_member_event_time)
        self.assertEqual(expected_public_message_event_time, obtained_public_message_event_time)
        self.assertEqual(expected_private_message_event_time, obtained_private_message_event_time)

    def test_get_message_text(self):
        """ Method for testing EventValidator.get_message_text """

        expected_public_member_event_message_text = self.PUBLIC_MEMBER_EVENT_MESSAGE_TEXT
        expected_public_message_event_message_text = self.PUBLIC_MESSAGE_EVENT_MESSAGE_TEXT
        expected_private_message_event_message_text = self.PRIVATE_MESSAGE_EVENT_MESSAGE_TEXT

        obtained_public_member_event_message_text = self.PublicMemberEventValidator.validated_internal_event.message
        obtained_public_message_event_message_text = self.PublicMessageEventValidator.validated_internal_event.message
        obtained_private_message_event_message_text = self.PrivateMessageEventValidator.validated_internal_event.message

        self.assertEqual(expected_public_member_event_message_text, obtained_public_member_event_message_text)
        self.assertEqual(expected_public_message_event_message_text, obtained_public_message_event_message_text)
        self.assertEqual(expected_private_message_event_message_text, obtained_private_message_event_message_text)
