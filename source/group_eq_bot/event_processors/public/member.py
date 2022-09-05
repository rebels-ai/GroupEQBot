from dataclasses import dataclass, field

from telegram.ext import ContextTypes
from telegram import ChatPermissions

from models.member import MemberStatus
from models.internal_event import ExpectedInternalEvent

from databases.events_driven_database.interfaces.documents.user import EventsDatabaseUserInterface
from databases.events_driven_database.interfaces.documents.chat import EventsDatabaseChatInterface
from databases.events_driven_database.interfaces.documents.event import EventsDatabaseEventInterface


from internal_logger.logger import logger


@dataclass
class MemberEventProcessor:
    """ Main Interface to process Member Updates. """

    internal_event: ExpectedInternalEvent
    context: ContextTypes.DEFAULT_TYPE

    welcome_message_for_conversation_handler: str = field(init=False)

    def __post_init__(self):
        """ Post initializer will retrieve and set from passed MemberEvent related values. """
        self.welcome_message_for_conversation_handler = f'Welcome on board @{self.internal_event.username} ! \n' \
                                                        f'Before to start enjoying tne chat, please introduce yourself answering couple of the questions. \n' \
                                                        f'Click on "/start" to initiate conversation. '

    async def process(self) -> None:
        """ Entrypoint for the MemberProcessor, which based on the StatusChange event, invoke appropriate logic. """

        logger.info('[MemberEventProcessor] is called ...')

        # either new member, who tries to join the group, who was not in the group before
        # or who was in the group in the past and left by (him/her)self
        # or who was removed from banned and added back to the group.
        if self.internal_event.old_status == MemberStatus.left \
                or self.internal_event.old_status == MemberStatus.banned \
                and self.internal_event.new_status == MemberStatus.member:

            logger.info('[MemberEventProcessor] attempting to write to database ...')
            EventsDatabaseEventInterface(internal_event=self.internal_event).process()
            EventsDatabaseUserInterface(internal_event=self.internal_event).process()
            EventsDatabaseChatInterface(internal_event=self.internal_event).process()

            await self.enable_restrictions_for_unvalidated_member()
            await self.context.bot.send_message(text=self.welcome_message_for_conversation_handler,
                                                chat_id=self.internal_event.chat_id)

        # validation was kicked off
        elif self.internal_event.old_status == MemberStatus.member \
                and self.internal_event.new_status == MemberStatus.restricted:

            logger.info('[MemberEventProcessor] attempting to write to database ...')
            EventsDatabaseEventInterface(internal_event=self.internal_event).process()
            EventsDatabaseUserInterface(internal_event=self.internal_event).process()
            EventsDatabaseChatInterface (internal_event=self.internal_event).process()

        # validation was passed successfully
        elif self.internal_event.old_status == MemberStatus.restricted \
                and self.internal_event.new_status == MemberStatus.member:

            logger.info('[MemberEventProcessor] attempting to write to database ...')
            EventsDatabaseEventInterface(internal_event=self.internal_event).process()
            EventsDatabaseUserInterface(internal_event=self.internal_event).process()
            EventsDatabaseChatInterface (internal_event=self.internal_event).process()

        # validation was not passed successfully, member left during validation process
        elif self.internal_event.old_status == MemberStatus.restricted \
                and self.internal_event.new_status == MemberStatus.restricted:

            logger.info('[MemberEventProcessor] attempting to write to database ...')
            EventsDatabaseEventInterface(internal_event=self.internal_event).process()
            EventsDatabaseUserInterface(internal_event=self.internal_event).process()
            EventsDatabaseChatInterface(internal_event=self.internal_event).process()

        # validation was failed, member was banned
        elif self.internal_event.old_status == MemberStatus.restricted \
                and self.internal_event.new_status == MemberStatus.banned:

            logger.info('[MemberEventProcessor] attempting to write to database ...')
            EventsDatabaseEventInterface(internal_event=self.internal_event).process()
            EventsDatabaseUserInterface(internal_event=self.internal_event).process()
            EventsDatabaseChatInterface(internal_event=self.internal_event).process()

        # member left the group by (him/her)self after passed validation
        elif self.internal_event.old_status == MemberStatus.member \
                and self.internal_event.new_status == MemberStatus.left:

            logger.info('[MemberEventProcessor] attempting to write to database ...')
            EventsDatabaseEventInterface(internal_event=self.internal_event).process()
            EventsDatabaseUserInterface(internal_event=self.internal_event).process()
            EventsDatabaseChatInterface(internal_event=self.internal_event).process()

        # member was banned by administrator of the group
        elif self.internal_event.old_status == MemberStatus.member \
                and self.internal_event.new_status == MemberStatus.banned:

            logger.info('[MemberEventProcessor] attempting to write to database ...')
            EventsDatabaseEventInterface(internal_event=self.internal_event).process()
            EventsDatabaseUserInterface(internal_event=self.internal_event).process()
            EventsDatabaseChatInterface(internal_event=self.internal_event).process()

        # member was removed from banned members by the administrator, but not added in the group back
        elif self.internal_event.old_status == MemberStatus.banned \
                and self.internal_event.new_status == MemberStatus.left:

            logger.info('[MemberEventProcessor] attempting to write to database ...')
            EventsDatabaseEventInterface(internal_event=self.internal_event).process()
            EventsDatabaseUserInterface(internal_event=self.internal_event).process()
            EventsDatabaseChatInterface(internal_event=self.internal_event).process()

        # unknown member event occurred
        else:
            EventsDatabaseEventInterface(internal_event=self.internal_event).process()
            EventsDatabaseUserInterface(internal_event=self.internal_event).process()
            EventsDatabaseChatInterface(internal_event=self.internal_event).process()
            logger.warning('Unknown member event occurred'
                           f'{self.internal_event}')
        return

    async def enable_restrictions_for_unvalidated_member(self):
        """ Function, which changes status from member on restricted,
        enabling restrictions for user, who started validation process. """

        await self.context.bot.restrict_chat_member(
            chat_id=self.internal_event.chat_id,
            user_id=self.internal_event.user_id,

            permissions=ChatPermissions(
                can_send_messages=True,  # to be able to reply ConversationHandler messages
                can_send_other_messages=False,
                can_invite_users=False,
                can_send_polls=False,
                can_send_media_messages=False,
                can_change_info=False,
                can_pin_messages=False,
                can_add_web_page_previews=False
            )
        )

