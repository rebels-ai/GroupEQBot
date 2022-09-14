# GroupEQBot Models

GroupEQBot utilises various data models on different processing stages.

Mainly, there are following ones:
- external_event
- internal_event
- validation


### external_event
##### event.ExpectedExternalEvent
- Model stands for describing any incoming TelegramEvent
```python
Example:
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
```



### internal_event
##### event.ExpectedInternalEvent
- Model stands for validated and processed ExpectedExternalEvent
```python
class ExpectedInternalEvent(BaseModel):
    """ Internal event data model definition. """

    class Config:
        extra = 'allow'
        arbitrary_types_allowed = True

    event: ExpectedExternalEvent
    event_type: EventType
    event_time: float  # datetime converted into POSIX timestamp

    chat_id: int
    chat_type: ChatType
    chat_name: str

    user_id: int
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    new_status: Optional[MemberStatus]
    old_status: Optional[MemberStatus]

    message_id: Optional[int]  # refer to router.router_helper.get_message_id
    message: Optional[str]
```

### validation
##### questions.Questions
- Model stands for question data model, which is supposed to be used in ConversationHandler
```python
class Questions(BaseModel):
    """ Questions data model, which is supposed to be used in ConversationHandler. """
    questions: List[Question]
```