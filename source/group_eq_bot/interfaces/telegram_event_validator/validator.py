from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from pydantic import ValidationError
from telegram import Update as TelegramEvent

from interfaces.models.internal_event.chat_type import ChatType
from interfaces.models.internal_event.event_type import EventType
from interfaces.models.internal_event.member_status import MemberStatus

from interfaces.models.external_event.event import ExpectedExternalEvent
from interfaces.models.internal_event.event import ExpectedInternalEvent

from utilities.internal_logger.logger import logger


@dataclass
class EventValidator:
    """ Helper interface for router to retrieve basic metadata of the event. """

    CHAT_NAME_IF_PRIVATE_MESSAGE_TYPE = 'group-eq-bot-private-chat'

    external_event: TelegramEvent
    validated_external_event: ExpectedExternalEvent = field(init=False)
    validated_internal_event: ExpectedInternalEvent = field(init=False)

    def __post_init__(self):
        self.validate_external_event()

        self.generate_internal_event()

    def validate_external_event(self):
        """ Function, which validates incoming TelegramEvent event with ExpectedExternalEvent. """
        try:
            logger.info('[EventValidator] Attempting to validate TelegramEvent against ExpectedExternalEvent.')
            self.validated_external_event = ExpectedExternalEvent(**self.external_event.to_dict())
            logger.info('[EventValidator] Successfully validated TelegramEvent against ExpectedExternalEvent.')
        except ValidationError as error:
            logger.warning('[EventValidator] Failed validating TelegramEvent against ExpectedExternalEvent.')
            raise error

    def generate_internal_event(self):
        logger.info('[EventValidator] Attempting to cast ExpectedExternalEvent into ExpectedInternalEvent.')
        self.validated_internal_event = ExpectedInternalEvent(event=self.validated_external_event,
                                                              chat_type=self.get_chat_type(),
                                                              event_type=self.get_event_type(),
                                                              chat_name=self.get_chat_name(),
                                                              chat_id=self.get_chat_id(),
                                                              user_id=self.get_user_id(),
                                                              message_id=self.get_message_id(),
                                                              first_name=self.get_user_first_name(),
                                                              last_name=self.get_user_last_name(),
                                                              username=self.get_username(),
                                                              new_status=self.get_user_new_status(),
                                                              old_status=self.get_user_old_status(),
                                                              event_time=self.get_event_time(),
                                                              message=self.get_message_text())
        logger.info('[EventValidator] Successfully casted ExpectedExternalEvent into ExpectedInternalEvent.')

    def get_chat_type(self) -> ChatType:
        """ Function to get chat_type from Message|Member event. """

        message = self.validated_external_event.message
        bot = self.validated_external_event.my_chat_member
        member = self.validated_external_event.chat_member
        
        if message:
           return self._retrieve_chat_type(chat_type=message.chat.type)
                      
        elif bot:
            return self._retrieve_chat_type(chat_type=bot.chat.type)
        
        elif member:
            return self._retrieve_chat_type(chat_type=bot.chat.type)
    
    @staticmethod
    def _retrieve_chat_type(chat_type: str):
        if ChatType.group.value == chat_type:
            return ChatType.group

        elif ChatType.supergroup.value == chat_type:
            return ChatType.supergroup

        elif ChatType.private.value == chat_type:
            return ChatType.private

    def get_event_type(self) -> EventType:
        """ Function to get event_type from Message | Member | Bot event. """

        if self.validated_external_event.message:
            return EventType.message
        
        elif self.validated_external_event.chat_member:
            return EventType.member    
        
        elif self.validated_external_event.my_chat_member:
            return EventType.bot

    def get_chat_name(self) -> str:
        """ Function to get chat_name from Message|Member event. """

        try:
            # [PUBLIC] MessageEvent
            chat_name = self.validated_external_event.message.chat.title
            # [PRIVATE] MessageEvent
            chat_name = self.CHAT_NAME_IF_PRIVATE_MESSAGE_TYPE if chat_name is None else chat_name
        except AttributeError:
            # [PUBLIC] MemberEvent
            chat_name = self.validated_external_event.chat_member.chat.title

        return chat_name

    def get_chat_id(self) -> int:
        """ Function to get chat_id from Message|Member event.
        Note:
            public chat id: denoted with minus (e.g.: -1001609170602)
            private chat id: denoted with plus (e.g.: 249785414)
        """

        try:
            # [PUBLIC | PRIVATE] MessageEvent
            chat_id = self.validated_external_event.message.chat.id
        except AttributeError:
            # [PUBLIC] MemberEvent
            chat_id = self.validated_external_event.chat_member.chat.id

        return chat_id

    def get_user_id(self) -> int:
        """ Function to get user_id from Message|Member event. """

        try:
            # [PUBLIC | PRIVATE] MessageEvent
            user_id = self.validated_external_event.message.from_user.id
        except AttributeError:
            # [PUBLIC] MemberEvent
            user_id = self.validated_external_event.chat_member.new_chat_member.user.id

        return user_id

    def get_message_id(self) -> int:
        """ Function to get message_id from Message|Member event.
        Note:
            if memberEvent occurred, message_id won't be provided by Telegram
            hence, None value will be declared. Further, with Elastic None will be casted.
        """

        try:
            # [PUBLIC | PRIVATE] MessageEvent
            message_id = self.validated_external_event.message.message_id
        except AttributeError:
            # [PUBLIC] MemberEvent
            message_id = None

        return message_id

    def get_user_first_name(self) -> str:
        """ Function to get first name from Message|Member event.

        Note:
            TelegramEvent(ExpectedExternalEvent) 'first_name' key is always presented 
        """

        try:
            # [PUBLIC | PRIVATE] MessageEvent
            first_name = self.validated_external_event.message.from_user.first_name
        except AttributeError:
            # [PUBLIC] MemberEvent
            first_name = self.validated_external_event.chat_member.new_chat_member.user.first_name

        return first_name

    def get_user_last_name(self) -> Optional[str]:
        """ Function to get last name from Message|Member event. 
        
        Note:
            TelegramEvent(ExpectedExternalEvent) 'last_name' key is optional (can be either None or str)
        """

        try:
            # [PUBLIC | PRIVATE] MessageEvent
            last_name = self.validated_external_event.message.from_user.last_name
        except AttributeError:
            last_name = None
        
        if last_name is None:
            try:
                # [PUBLIC] MemberEvent
                last_name = self.validated_external_event.chat_member.new_chat_member.user.last_name
            except AttributeError:
                last_name = None

        return last_name
    
    def get_username(self) -> Optional[str]:
        """ Function to get username from Message|Member event. """

        try:
            # [PUBLIC | PRIVATE] MessageEvent
            username = self.validated_external_event.message.from_user.username
        except AttributeError:
            username = None

        if username is None:
            try:
                # [PUBLIC] MemberEvent
                username = self.validated_external_event.chat_member.new_chat_member.user.username
            except AttributeError:
                username = None

        return username

    def get_user_new_status(self) -> Optional[MemberStatus]:
        """ Function to get user new_status from Message|Member event. """

        try:
            # [PUBLIC] MemberEvent
            status = self.validated_external_event.chat_member.new_chat_member.status
        except AttributeError:
            # [PUBLIC | PRIVATE] MessageEvent
            status = None

        return MemberStatus(status)

    def get_user_old_status(self) -> Optional[MemberStatus]:
        """ Function to get user old_status from Message|Member event. """

        try:
            # [PUBLIC] MemberEvent
            status = self.validated_external_event.chat_member.old_chat_member.status
        except AttributeError:
            # [PUBLIC | PRIVATE] MessageEvent
            status = None

        return MemberStatus(status)

    def get_event_time(self) -> float:
        """ Function to get time from Message|Member event. """

        try:
            # [PUBLIC] MemberEvent
            date = self.validated_external_event.chat_member.date
        except AttributeError:
            # [PUBLIC | PRIVATE] MessageEvent
            date = self.validated_external_event.message.date

        try:
            timestamp = datetime.timestamp(date)
        except OverflowError as error:
            raise error

        return timestamp

    def get_message_text(self) -> Optional[str]:
        """ Function to get user message content from Message|Member event. """

        try:
            # [PUBLIC | PRIVATE] MessageEvent
            message_text = self.validated_external_event.message.text
        except AttributeError:
            # [PUBLIC] MemberEvent
            message_text = None

        return message_text
