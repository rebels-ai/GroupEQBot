from datetime import datetime
from typing import Optional, Union, List
from pydantic import BaseModel, Field, validator


class User(BaseModel):
    """
    https://core.telegram.org/bots/api#user
    This object represents a Telegram user or bot.
    """
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = None


class ChatPhoto(BaseModel):
    """
    https://core.telegram.org/bots/api#chatphoto
    This object represents a chat photo.
    """
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str


class ChatPermissions(BaseModel):
    """
    https://core.telegram.org/bots/api#chatpermissions
    Describes actions that a non-administrator user
    is allowed to take in a chat.
    """
    can_send_messages: Optional[bool] = None
    can_send_media_messages: Optional[bool] = None
    can_send_polls: Optional[bool] = None
    can_send_other_messages: Optional[bool] = None
    can_add_web_page_previews: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_pin_messages: Optional[bool] = None


class Location(BaseModel):
    """
    https://core.telegram.org/bots/api#location
    This object represents a point on the map.
    """
    longitude: float
    latitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None

    @validator('horizontal_accuracy')
    def size_horizontal_accuracy_must_contain_a_range(cls, v):
        if v < 0 or v > 1500:
            raise ValueError('Must contain a range of 0 - 1500')


class ChatLocation(BaseModel):
    """
    https://core.telegram.org/bots/api#chatlocation
    Represents a location to which a chat is connected.
    """
    location: Location
    address: str


class Chat(BaseModel):
    """
    https://core.telegram.org/bots/api#chat
    This object represents a chat.
    """
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo: Optional[ChatPhoto] = None
    bio: Optional[str] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional['Message'] = None
    permissions: Optional[ChatPermissions] = None
    slow_mode_delay: Optional[int] = None
    message_auto_delete_time: Optional[int] = None
    sticker_set_name: Optional[str] = None
    can_set_sticker_set: Optional[bool] = None
    linked_chat_id: Optional[int] = None
    location: Optional[ChatLocation] = None


class MessageEntity(BaseModel):
    """
    https://core.telegram.org/bots/api#messageentity
    This object represents one special entity in a text message.
     For example, hashtags, usernames, URLs, etc.
    """
    type: str
    offset: int
    length: int
    url: Optional[str] = None
    user: Optional[User] = None
    language: Optional[str] = None


class PhotoSize(BaseModel):
    """
    https://core.telegram.org/bots/api#photosize
    This object represents one size of a photo or a file / sticker thumbnail.
    """
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int] = None


class Animation(BaseModel):
    """
    https://core.telegram.org/bots/api#animation
    This object represents an animation file
    (GIF or H.264/MPEG-4 AVC video without sound).
    """
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


class Audio(BaseModel):
    """
    https://core.telegram.org/bots/api#audio
    This object represents an audio file
    to be treated as music by the Telegram clients.
    """
    file_id: str
    file_unique_id: str
    duration: int
    performer: Optional[str] = None
    title: Optional[str] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    thumb: Optional[PhotoSize] = None


class Document(BaseModel):
    """
    https://core.telegram.org/bots/api#document
    This object represents a general file
    (as opposed to photos, voice messages and audio files).
    """
    file_id: str
    file_unique_id: str
    thumb: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


class Sticker(BaseModel):
    """
    https://core.telegram.org/bots/api#sticker
    This object represents a sticker.
    """
    file_id: str
    file_unique_id: str
    width: int
    height: int
    is_animated: bool
    thumb: Optional[PhotoSize] = None
    emoji: Optional[str] = None
    set_name: Optional[str] = None
    mask_position: Optional[str] = None
    file_size: Optional[int] = None


class Video(BaseModel):
    """
    https://core.telegram.org/bots/api#video
    This object represents a video file.
    """
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


class VideoNote(BaseModel):
    """
    https://core.telegram.org/bots/api#videonote
    This object represents a video message
    (available in Telegram apps as of v.4.0).
    """
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumb: Optional[PhotoSize] = None
    file_size: Optional[int] = None


class Voice(BaseModel):
    """
    https://core.telegram.org/bots/api#voice
    This object represents a voice note.
    """
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


class Contact(BaseModel):
    """
    https://core.telegram.org/bots/api#contact
    This object represents a phone contact.
    """
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    user_id: Optional[str] = None
    vcard: Optional[str] = None


class Dice(BaseModel):
    """
    https://core.telegram.org/bots/api#dice
    This object represents an animated emoji that displays a random value.
    """
    emoji: str
    value: int


class Game(BaseModel):
    """
    https://core.telegram.org/bots/api#game
    This object represents a game.
    Use BotFather to create and edit games,
    their short names will act as unique identifiers.
    """
    title: str
    description: str
    photo: Union[list, PhotoSize, None] = None
    text: Optional[str] = None
    text_entities: Union[list, MessageEntity, None] = None
    animation: Optional[Animation] = None


class PollOption(BaseModel):
    """
    https://core.telegram.org/bots/api#polloption
    This object contains information about one answer option in a poll.
    """
    text: str
    voter_count: int


class Poll(BaseModel):
    """
    https://core.telegram.org/bots/api#poll
    This object contains information about a poll.
    """
    id: str
    question: str
    options: Union[list, PollOption, None] = None
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool
    correct_option_id: Optional[int] = None
    explanation: Optional[str] = None
    explanation_entities: Union[list, MessageEntity, None] = None
    open_period: Optional[int] = None
    close_date: Optional[int] = None

    @validator('question')
    def question_characters_limit(cls, v):
        if len(v) > 300:
            raise ValueError('question limited 300 characters')


class MessageAutoDeleteTimerChanged(BaseModel):
    """
    https://core.telegram.org/bots/api#messageautodeletetimerchanged
    This object represents a service message
    about a change in auto-delete timer settings.
    """
    message_auto_delete_time: int


class Venue(BaseModel):
    """
    https://core.telegram.org/bots/api#venue
    This object represents a venue.
    """
    location: Location
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None


class Invoice(BaseModel):
    """
    https://core.telegram.org/bots/api#invoice
    This object contains basic information about an invoice.
    """
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int


class ShippingAddress(BaseModel):
    """
    https://core.telegram.org/bots/api#shippingaddress
    This object represents a shipping address.
    """
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str


class OrderInfo(BaseModel):
    """
    https://core.telegram.org/bots/api#orderinfo
    This object represents information about an order.
    """
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    shipping_address: Optional[ShippingAddress] = None


class SuccessfulPayment(BaseModel):
    """
    https://core.telegram.org/bots/api#successfulpayment
    This object contains basic information about a successful payment.
    """
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None
    telegram_payment_charge_id: str
    provider_payment_charge_id: str


class PassportFile(BaseModel):
    """
    https://core.telegram.org/bots/api#passportfile
    This object represents a file uploaded to Telegram Passport.
     Currently all Telegram Passport files are in JPEG
     format when decrypted and don't exceed 10MB.
    """
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int


class EncryptedPassportElement(BaseModel):
    """
    https://core.telegram.org/bots/api#encryptedpassportelement
    Contains information about documents or
    other Telegram Passport elements shared with the bot by the user.
    """
    type: str
    data: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    files: Union[list, PassportFile, None] = None
    front_side: Optional[PassportFile] = None
    reverse_side: Optional[PassportFile] = None
    selfie: Optional[PassportFile] = None
    translation: Union[list, PassportFile, None] = None
    hash: str


class EncryptedCredentials(BaseModel):
    """
    https://core.telegram.org/bots/api#encryptedcredentials
    Contains data required for decrypting
    and authenticating EncryptedPassportElement.
    See the Telegram Passport Documentation
    for a complete description of the data decryption
    and authentication processes.
    """
    data: str
    hash: str
    secret: str


class PassportData(BaseModel):
    """
    https://core.telegram.org/bots/api#passportdata
    Contains information
    about Telegram Passport data shared with the bot by the user.
    """
    data: Union[list, EncryptedPassportElement]
    credentials: EncryptedCredentials


class ProximityAlertTriggered(BaseModel):
    """
    https://core.telegram.org/bots/api#proximityalerttriggered
    This object represents the content of a service message,
    sent whenever a user in the chat triggers a proximity
    alert set by another user.
    """
    traveler: User
    watcher: User
    distance: int


class VoiceChatScheduled(BaseModel):
    """
    https://core.telegram.org/bots/api#voicechatscheduled
    This object represents the content of a service message,
    sent whenever a user in the chat triggers
     a proximity alert set by another user.
    """
    start_date: int


class VoiceChatStarted(BaseModel):
    """
    https://core.telegram.org/bots/api#voicechatstarted
    This object represents a service message
     about a voice chat started in the chat.
     Currently holds no information.
    """
    pass


class VoiceChatEnded(BaseModel):
    """
    https://core.telegram.org/bots/api#voicechatended
    This object represents a service message
    about a voice chat ended in the chat.
    """
    duration: int


class VoiceChatParticipantsInvited(BaseModel):
    """
    https://core.telegram.org/bots/api#voicechatparticipantsinvited
    This object represents a service message
    about new members invited to a voice chat.
    """
    users: Union[list, User, None] = None


class LoginUrl(BaseModel):
    """
    https://core.telegram.org/bots/api#loginurl
    This object represents
     a parameter of the inline keyboard button
      used to automatically authorize a user.
    Serves as a great replacement for the Telegram Login Widget
    when the user is coming from Telegram.
    All the user needs to do is tap/click a button
    and confirm that they want to log in.
    """
    url: str
    forward_text: Optional[str] = None
    bot_username: Optional[str] = None
    request_write_access: Optional[bool] = None


class CallbackGame(BaseModel):
    """
    https://core.telegram.org/bots/api#callbackgame
    A placeholder, currently holds no information.
    Use BotFather to set up your game.
    """
    pass


class InlineKeyboardButton(BaseModel):
    """
    https://core.telegram.org/bots/api#inlinekeyboardbutton
    This object represents one button of an inline keyboard.
    You must use exactly one of the optional fields.
    """
    text: str
    url: Optional[str]
    login_url: Optional[LoginUrl] = None
    callback_data: Optional[str] = None
    switch_inline_query: Optional[str] = None
    switch_inline_query_current_chat: Optional[str] = None
    callback_game: Optional[CallbackGame] = None
    pay: Optional[bool]


class ForceReply(BaseModel):
    """
    https://core.telegram.org/bots/api#forcereply
    Upon receiving a message with this object,
    Telegram clients will display a reply interface to the user
    (act as if the user has selected the bot's message and tapped 'Reply')
    """
    force_reply: bool = True
    input_field_placeholder: Optional[str]
    selective: Optional[bool]


class ReplyKeyboardRemove(BaseModel):
    """
    https://core.telegram.org/bots/api#replykeyboardremove
    Upon receiving a message with this object, Telegram clients
    will remove the current custom keyboard and display
    the default letter-keyboard.
    """
    remove_keyboard: bool = True
    selective: Optional[bool]


class KeyboardButtonPollType(BaseModel):
    """
    https://core.telegram.org/bots/api#keyboardbuttonpolltype
    This object represents type of a poll, which is allowed to be
    created and sent when the corresponding button is pressed.
    """
    type: Optional[str] = None


class WebAppInfo(BaseModel):
    """
    https://core.telegram.org/bots/api#webappinfo
    Contains information about a Web App.
    """
    url: Optional[str] = None


class KeyboardButton(BaseModel):
    """
    https://core.telegram.org/bots/api#keyboardbutton
    This object represents one button of the reply keyboard.
    """
    text: str
    request_contact: Optional[bool]
    request_location: Optional[bool]
    request_poll: Optional[KeyboardButtonPollType]
    web_app: Optional[WebAppInfo]


class InlineKeyboardMarkup(BaseModel):
    """
    https://core.telegram.org/bots/api#inlinekeyboardmarkup
    This object represents an inline keyboard that appears
    right next to the message it belongs to.
    """
    inline_keyboard: Union[list, List[InlineKeyboardButton]]


class ReplyKeyboardMarkup(BaseModel):
    """
    https://core.telegram.org/bots/api#replykeyboardmarkup
    This object represents a custom keyboard with reply options
    """
    keyboard: Union[list, List[KeyboardButton]]
    resize_keyboard: Optional[bool]
    one_time_keyboard: Optional[bool]
    input_field_placeholder: Optional[str]
    selective: Optional[bool]


class MessageToSend(BaseModel):
    """
    https://core.telegram.org/bots/api#sendmessage
    Message data to use sendMessage method
    """
    chat_id: Union[str, int]
    text: str
    parse_mode: Optional[str] = None
    entities: Union[list, MessageEntity, None] = None
    disable_web_page_preview: Optional[bool] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    reply_to_message_id: Optional[int] = None
    allow_sending_without_reply: Optional[bool] = None
    reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup,
                        ReplyKeyboardRemove, ForceReply, None] = None


class Message(BaseModel):
    """
    https://core.telegram.org/bots/api#message
    This object represents a message.
    """
    message_id: int
    from_user: Optional[User] = Field(None, alias='from')
    sender_chat: Optional[Chat] = None
    date: datetime
    chat: Chat
    forward_from: Optional[User] = None
    forward_from_chat: Optional[Chat] = None
    forward_from_message_id: Optional[int] = None
    forward_signature: Optional[str] = None
    forward_sender_name: Optional[str] = None
    forward_date: Optional[int] = None
    reply_to_message: Optional['Message'] = None
    via_bot: Optional[User] = None
    edit_date: Optional[int] = None
    media_group_id: Optional[str] = None
    author_signature: Optional[str] = None
    text: Optional[str] = None
    entities: Union[list, MessageEntity, None] = None
    animation: Optional[Animation] = None
    audio: Optional[Audio] = None
    document: Optional[Document] = None
    photo: Union[list, PhotoSize, None] = None
    sticker: Optional[Sticker] = None
    video: Optional[Video] = None
    video_note: Optional[VideoNote] = None
    voice: Optional[Voice] = None
    caption: Optional[str] = None
    caption_entities: Union[list, MessageEntity, None] = None
    contact: Optional[Contact] = None
    dice: Optional[Dice] = None
    game: Optional[Game] = None
    poll: Optional[Poll] = None
    venue: Optional[Venue] = None
    location: Optional[Location] = None
    new_chat_members: Union[list, User, None] = None
    left_chat_member: Optional[User] = None
    new_chat_title: Optional[str] = None
    new_chat_photo: Union[list, PhotoSize, None] = None
    delete_chat_photo: Optional[bool] = None
    group_chat_created: Optional[bool] = None
    supergroup_chat_created: Optional[bool] = None
    channel_chat_created: Optional[bool] = None
    message_auto_delete_timer_changed: \
        Optional[MessageAutoDeleteTimerChanged] = None
    migrate_to_chat_id: Optional[int] = None
    migrate_from_chat_id: Optional[int] = None
    pinned_message: Optional['Message'] = None
    invoice: Optional[Invoice] = None
    successful_payment: Optional[SuccessfulPayment] = None
    connected_website: Optional[str] = None
    passport_data: Optional[PassportData] = None
    proximity_alert_triggered: Optional[ProximityAlertTriggered] = None
    voice_chat_scheduled: Optional[VoiceChatScheduled] = None
    voice_chat_started: Optional[VoiceChatStarted] = None
    voice_chat_ended: Optional[VoiceChatEnded] = None
    voice_chat_participants_invited: \
        Optional[VoiceChatParticipantsInvited] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None


class InlineQuery(BaseModel):
    """
    https://core.telegram.org/bots/api#inlinequery
    This object represents an incoming inline query.
     When the user sends an empty query,
     your bot could return some default or trending results.
    """
    id: str
    from_user: User = Field(alias='from')
    query: str
    offset: str
    chat_type: Optional[str] = None
    location: Optional[Location] = None

    @validator('query')
    def query_characters_limit(cls, v):
        if len(v) > 256:
            raise ValueError('query limited 256 characters')


class ChosenInlineResult(BaseModel):
    """
    https://core.telegram.org/bots/api#choseninlineresult
    Represents a result of an inline query
    that was chosen by the user and sent to their chat partner.
    """
    result_id: str
    from_user: User = Field(alias='from')
    location: Optional[Location] = None
    inline_message_id: Optional[str] = None
    query: str


class CallbackQuery(BaseModel):
    """
    https://core.telegram.org/bots/api#callbackquery
    This object represents
     an incoming callback query from a callback button
      in an inline keyboard.
    If the button that originated the query was attached
     to a message sent by the bot, the field message will be present.
    If the button was attached to a message sent
     via the bot (in inline mode),
     the field inline_message_id will be present.
    Exactly one of the fields data
    or game_short_name will be present.
    """
    id: str
    from_user: User = Field(alias='from')
    message: Optional[Message] = None
    inline_message_id: Optional[str] = None
    chat_instance: str
    data: Optional[str] = None
    game_short_name: Optional[str] = None


class ShippingQuery(BaseModel):
    """
    https://core.telegram.org/bots/api#shippingquery
    This object contains information about an incoming shipping query.
    """
    id: str
    from_user: User = Field(alias='from')
    invoice_payload: str
    shipping_address: ShippingAddress


class PreCheckoutQuery(BaseModel):
    """
    https://core.telegram.org/bots/api#precheckoutquery
    This object contains information about an incoming pre-checkout query.
    """
    id: str
    from_user: User = Field(alias='from')
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None


class PollAnswer(BaseModel):
    """
    https://core.telegram.org/bots/api#pollanswer
    This object represents an answer of a user in a non-anonymous poll.
    """
    poll_id: str
    user: User
    option_ids: Union[list, int]


class ChatMemberOwner(BaseModel):
    """
    https://core.telegram.org/bots/api#chatmemberowner
    Represents a chat member
     that owns the chat and has all administrator privileges.
    """
    status: str
    user: User
    is_anonymous: bool
    custom_title: Optional[str] = None


class ChatMemberAdministrator(BaseModel):
    """
    https://core.telegram.org/bots/api#chatmemberadministrator
    Represents a chat member that has some additional privileges.
    """
    status: str
    user: User
    can_be_edited: bool
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_voice_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    custom_title: Optional[str] = None


class ChatMemberMember(BaseModel):
    """
    https://core.telegram.org/bots/api#chatmembermember
    Represents a chat member that has no additional privileges
    or restrictions.
    """
    status: str
    user: User


class ChatMemberRestricted(BaseModel):
    """
    https://core.telegram.org/bots/api#chatmemberrestricted
    Represents a chat member that is under
     certain restrictions in the chat. Supergroups only.
    """
    status: str
    user: User
    is_member: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_send_messages: bool
    can_send_media_messages: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_previews: bool
    until_date: datetime


class ChatMemberLeft(BaseModel):
    """
    https://core.telegram.org/bots/api#chatmemberleft
    Represents a chat member that isn't currently a member of the chat,
     but may join it themselves.
    """
    status: str
    user: User


class ChatMemberBanned(BaseModel):
    """
    https://core.telegram.org/bots/api#chatmemberbanned
    Represents a chat member
    that was banned in the chat and can't
    return to the chat or view chat messages.
    """
    status: str
    user: User
    until_date: int


class ChatInviteLink(BaseModel):
    """
    https://core.telegram.org/bots/api#chatinvitelink
    Represents an invite link for a chat.
    """
    invite_link: str
    creator: User
    is_primary: bool
    is_revoked: bool
    expire_date: Optional[int] = None
    member_limit: Optional[int] = None


class ChatMemberUpdated(BaseModel):
    """
    https://core.telegram.org/bots/api#chatmemberupdated
    This object represents changes in the status of a chat member.
    """
    chat: Chat
    from_user: User = Field(alias='from')
    date: datetime
    old_chat_member: Union[
        ChatMemberOwner, ChatMemberAdministrator,
        ChatMemberMember, ChatMemberRestricted,
        ChatMemberLeft, ChatMemberBanned]
    new_chat_member: Union[
        ChatMemberOwner, ChatMemberAdministrator,
        ChatMemberMember, ChatMemberRestricted,
        ChatMemberLeft, ChatMemberBanned]
    invite_link: Optional[ChatInviteLink]


class ExpectedExternalEvent(BaseModel):
    """
    https://core.telegram.org/bots/api#update
    This object represents an incoming update from Telegram, but is defined within our system to control further updates
      from Telegram.
    At most one of the optional parameters can be present in any given update.
    """
    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None
    inline_query: Optional[InlineQuery] = None
    chosen_inline_result: Optional[ChosenInlineResult] = None
    callback_query: Optional[CallbackQuery] = None
    shipping_query: Optional[ShippingQuery] = None
    pre_checkout_query: Optional[PreCheckoutQuery] = None
    poll: Optional[Poll] = None
    poll_answer: Optional[PollAnswer] = None
    my_chat_member: Optional[ChatMemberUpdated] = None
    chat_member: Optional[ChatMemberUpdated] = None