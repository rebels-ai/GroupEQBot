from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field

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
        """ Function, which generates InternalEvent, extracting some data from ExternalEvent. """

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

    def get_chat_type(self) -> str:
        """ Function to get chat_type from Message|Member event. """

        message = self.validated_external_event.message
        bot = self.validated_external_event.my_chat_member
        member = self.validated_external_event.chat_member
        
        if message:
            return self._retrieve_chat_type(chat_type=message.chat.type)
                      
        elif bot:
            return self._retrieve_chat_type(chat_type=bot.chat.type)
        
        elif member:
            return self._retrieve_chat_type(chat_type=member.chat.type)
    
    @staticmethod
    def _retrieve_chat_type(chat_type: str) -> str:
        """ Function, which returns ChatType model depending on value provided . """

        if ChatType.supergroup.value == chat_type:
            return ChatType.supergroup.value

        elif ChatType.private.value == chat_type:
            return ChatType.private.value

    def get_event_type(self) -> str:
        """ Function to get event_type from Message | Member | Bot event. """

        if self.validated_external_event.message:
            return EventType.message.value
        
        elif self.validated_external_event.chat_member:
            return EventType.member.value
        
        elif self.validated_external_event.my_chat_member:
            return EventType.bot.value

    def get_chat_name(self) -> str:
        """ Function to get chat_name from Message | Member | Bot event. """

        message = self.validated_external_event.message
        bot = self.validated_external_event.my_chat_member
        member = self.validated_external_event.chat_member

        if message:
            return message.chat.title if message.chat.title is not None else self.CHAT_NAME_IF_PRIVATE_MESSAGE_TYPE

        elif bot:
            return bot.chat.title if bot.chat.title is not None else self.CHAT_NAME_IF_PRIVATE_MESSAGE_TYPE

        elif member:
            return member.chat.title

    def get_chat_id(self) -> int:
        """ Function to get chat_id from Message | Member | Bot event.
        Note:
            public chat id: denoted with minus (e.g.: -1001609170602)
            private chat id: denoted with plus (e.g.: 249785414)
        """

        message = self.validated_external_event.message
        bot = self.validated_external_event.my_chat_member
        member = self.validated_external_event.chat_member

        if message:
            return message.chat.id

        elif bot:
            return bot.chat.id
        
        elif member:
            return member.chat.id

    def get_user_id(self) -> int:
        """ Function to get user_id from Message | Member | Bot event. """

        message = self.validated_external_event.message
        bot = self.validated_external_event.my_chat_member
        member = self.validated_external_event.chat_member

        if message:
            return message.from_user.id

        elif bot:
            return bot.new_chat_member.user.id  #

        elif member:
            return member.new_chat_member.user.id

    def get_message_id(self) -> Optional[int]:
        """ Function to get message_id from Message | Member | Bot event.
        Note:
            if memberEvent occurred, message_id won't be provided by Telegram
            hence, None value will be declared. Further, with Elastic None will be casted.
        """

        message = self.validated_external_event.message

        if message:
            return message.message_id

        else:
            return None

    def get_user_first_name(self) -> str:
        """ Function to get first name from Message | Member | Bot event.

        Note:
            TelegramEvent(ExpectedExternalEvent) 'first_name' key is always presented
        """

        message = self.validated_external_event.message
        bot = self.validated_external_event.my_chat_member
        member = self.validated_external_event.chat_member

        if message:
            return message.from_user.first_name

        elif bot:
            return bot.new_chat_member.user.first_name

        elif member:
            return member.new_chat_member.user.first_name

    def get_user_last_name(self) -> Optional[str]:
        """ Function to get last name from Message | Member | Bot event. 
        
        Note:
            TelegramEvent(ExpectedExternalEvent) 'last_name' key is optional (can be either None or str)
        """

        message = self.validated_external_event.message
        bot = self.validated_external_event.my_chat_member
        member = self.validated_external_event.chat_member

        if message:
            return message.from_user.last_name

        elif bot:
            return bot.new_chat_member.user.last_name

        elif member:
            return member.new_chat_member.user.last_name
    
    def get_username(self) -> Optional[str]:
        """ Function to get username from Message | Member | Bot event. """

        message = self.validated_external_event.message
        bot = self.validated_external_event.my_chat_member
        member = self.validated_external_event.chat_member

        if message:
            return message.from_user.username

        elif bot:
            return bot.new_chat_member.user.username

        elif member:
            return member.new_chat_member.user.username

    def get_user_new_status(self) -> Optional[str]:
        """ Function to get user new_status from Message | Member | Bot event. """

        message = self.validated_external_event.message
        bot = self.validated_external_event.my_chat_member
        member = self.validated_external_event.chat_member

        if message:
            return None

        elif bot:
            return MemberStatus(bot.new_chat_member.status).value
        
        elif member:
            return MemberStatus(member.new_chat_member.status).value

    def get_user_old_status(self) -> Optional[str]:
        """ Function to get user old_status from Message | Member | Bot event. """

        message = self.validated_external_event.message
        bot = self.validated_external_event.my_chat_member
        member = self.validated_external_event.chat_member

        if message:
            return None

        elif bot:
            return MemberStatus(bot.old_chat_member.status).value
        
        elif member:
            return MemberStatus(member.old_chat_member.status).value

    def get_event_time(self) -> datetime:
        """ Function to get time from Message | Member | Bot event. """

        message = self.validated_external_event.message
        bot = self.validated_external_event.my_chat_member
        member = self.validated_external_event.chat_member

        if message:
            date = message.date

        elif bot:
            date = bot.date
        
        elif member:
            date = member.date

        return date

    def get_message_text(self) -> Optional[str]:
        """ Function to get user message content from Message | Member | Bot event. """

        message = self.validated_external_event.message

        if message:
           return message.text

        else:
            return None
