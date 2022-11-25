from dataclasses import dataclass, field

from telegram import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from elasticsearch_dsl import Q
from interfaces.models.internal_event.member_status import MemberStatus
from interfaces.models.internal_event.event import ExpectedInternalEvent

from utilities.internal_logger.logger import logger
from utilities.configurations_constructor.constructor import Constructor

from storage.schemas.group_events.schema import Builder as EventBuilder
from storage.schemas.group_users.schema import Builder as UserBuilder, GroupUser
from storage.query.query import update_query, find_query
from storage.connectors.connector import connection


@dataclass
class MemberEventProcessor:
    """ Main Interface to process Member Updates. """

    internal_event: ExpectedInternalEvent
    context: ContextTypes.DEFAULT_TYPE
    configurator: Constructor = field(default_factory=lambda: Constructor())

    async def process(self) -> None:
        """ Entrypoint for the MemberProcessor, which based on the StatusChange event, invoke appropriate logic. """

        logger.info('[MemberEventProcessor] is called ...')

        # either new member, who tries to join the group, who was not in the group before
        # or who was in the group in the past and left by (him/her)self
        # or who was removed from banned and added back to the group.
        if self.internal_event.old_status == MemberStatus.left.value \
            or self.internal_event.old_status == MemberStatus.banned.value \
                and self.internal_event.new_status == MemberStatus.member.value:

            self._write_event_to_datase()
            self._write_user_to_database()

            # @TODO: Add member checking in DB
            # if validation.passed == True --> send welcome back message
            # if validation.passed == False --> enable restrictions --> send welcome message

            await self.enable_restrictions_for_unvalidated_member()

            await self.context.bot.send_message(
                reply_markup=self._get_reply_markup(),
                protect_content=True,
                parse_mode=ParseMode.MARKDOWN_V2,
                chat_id=self.internal_event.chat_id,
                text=self.configurator.configurations.bot.validation.welcome_message.replace('USERNAME', f'[{self.internal_event.first_name}](tg://user?id={self.internal_event.user_id})'))

            
        # validation was kicked off
        elif self.internal_event.old_status == MemberStatus.member.value \
                and self.internal_event.new_status == MemberStatus.restricted.value:
                self._write_event_to_datase()
                self._write_user_to_database()

        # validation was passed successfully
        elif self.internal_event.old_status == MemberStatus.restricted.value \
                and self.internal_event.new_status == MemberStatus.member.value:
                self._write_event_to_datase()
                self._write_user_to_database()

        # validation was failed, member was banned
        elif self.internal_event.old_status == MemberStatus.restricted.value \
                and self.internal_event.new_status == MemberStatus.banned.value:
                self._write_event_to_datase()
                self._write_user_to_database()

        # member left the group by (him/her)self before passing validation
        elif self.internal_event.old_status == MemberStatus.restricted.value \
            and self.internal_event.new_status == MemberStatus.restricted.value:
                self._write_event_to_datase()
                self._write_user_to_database()

        # member left the group by (him/her)self after passed validation
        elif self.internal_event.old_status == MemberStatus.member.value \
                and self.internal_event.new_status == MemberStatus.left.value:
                self._write_event_to_datase()
                self._write_user_to_database()

        # member was banned by administrator of the group
        elif self.internal_event.old_status == MemberStatus.member.value \
                and self.internal_event.new_status == MemberStatus.banned.value:
                self._write_event_to_datase()
                self._write_user_to_database()

        # member was removed from banned members by the administrator, but not added in the group back
        elif self.internal_event.old_status == MemberStatus.banned.value \
                and self.internal_event.new_status == MemberStatus.left.value:
                self._write_event_to_datase()
                self._write_user_to_database()

        # member left the group before passing validation and the administrator disabled restrictions
        elif self.internal_event.old_status == MemberStatus.restricted.value \
                and self.internal_event.new_status == MemberStatus.left.value:
                self._write_event_to_datase()
                self._write_user_to_database()

        # unknown member event occurred
        else:
            self._write_event_to_datase()
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
                can_send_messages=False,
                can_send_other_messages=False,
                can_invite_users=False,
                can_send_polls=False,
                can_send_media_messages=False,
                can_change_info=False,
                can_pin_messages=False,
                can_add_web_page_previews=False
            )
        )

    def _write_event_to_datase(self):
        logger.info('[MemberEventProcessor] attempting to write to storage ...')

        event_document = EventBuilder(object=self.internal_event).build()
        event_document.schema.save(index=event_document.index_name)

    def _write_user_to_database(self):
        logger.info('[MemberEventProcessor] attempting to write to storage ...')

        query = Q('match', user_id=self.internal_event.user_id)
        document = UserBuilder(object=self.internal_event).build()

        index = document.schema._get_index()
        user_document = find_query(query=query, index_name=document.index_name, doc_type=GroupUser)

        if index is None or len(user_document) == 0:
            document.schema.save(index=document.index_name)
        else:
            chat_id = abs(self.internal_event.chat_id)
            index_name = f'{GroupUser.Index.name}-group-users-{chat_id}'
            connection.indices.refresh(index=document.index_name)
            source = "ctx._source.event.status.current_status = params.current_status; ctx._source.event.status.change_history_status.add(params.change_history_status)"
            params = {"current_status": self.internal_event.new_status,
                      "change_history_status": {self.internal_event.new_status: self.internal_event.event_time}}
            update_query(query=query, index_name=index_name, doc_type=GroupUser, source=source, params=params)

    def _get_reply_markup(self):
        keyboard = [
            [InlineKeyboardButton(
                text=self.configurator.configurations.bot.validation.bot_button_text,
                 url=self.configurator.configurations.bot.general.url
                 )
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
