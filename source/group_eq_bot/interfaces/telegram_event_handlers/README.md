# GroupEQBot Handlers:

GroupEQBot handlers are the wrapper on top of native [Telegram Handlers](https://docs.python-telegram-bot.org/en/v20.0a4/telegram.ext.handlers-tree.html).

## Handler Interface Explanation
Any of the GroupEQBot handlers interface is declared as:
```python
class {"HandlerType"}Handler:
    filters_to_apply = { "Telegram filters to be used" }
    callback_to_call = { "Function which will be called once such an event will be registered" }

    handler = {According to required {"HandlerType"} Telegram}Handler(filters=filters_to_apply,
                             callback=callback_to_call)
```

VideoMessageHandler  Example:
```python
class VideoMessageHandler:
    filters_to_apply = filters.VIDEO | filters.VIDEO_NOTE | filters.Sticker.ALL | filters.ANIMATION | filters.PHOTO
    callback_to_call = route_event

    handler = MessageHandler(filters=filters_to_apply,
                             callback=callback_to_call)
```


## Handlers

#### Message Handlers
Handles `commands`, `text`, `audio`, `video`, `document`, `voice`, `video note`, `sticker`, `animation`, `photo` message types

##### Command Handler

*At this moment none of the standalone commands are registered.*
*There are two within conversation validation handler*
- Based on [Telegram Command Handler](https://docs.python-telegram-bot.org/en/v20.0a4/telegram.ext.basehandler.html)
- Stands for `registering` command messages like `/start`, `/end`, ...
- Callback function: 

##### Text Message Handler
- Based on [Telegram Message Handler](https://docs.python-telegram-bot.org/en/v20.0a4/telegram.ext.messagehandler.html)
- Stands for registering text messages, excluding commands
- Callback function: `interfaces.telegram_event_router.router.route_event`

##### Audio Message Handler
- Based on [Telegram Message Handler](https://docs.python-telegram-bot.org/en/v20.0a4/telegram.ext.messagehandler.html)
- Stands for registering audio and voice messages
- Callback function: `interfaces.telegram_event_router.router.route_event`

##### Video Message Handler
- Based on [Telegram Message Handler](https://docs.python-telegram-bot.org/en/v20.0a4/telegram.ext.messagehandler.html)
- Stands for registering messages, containing videos, video notes, stickers, animations and photos
- Callback function: `interfaces.telegram_event_router.router.route_event`

##### Document Message Handler
- Based on [Telegram Message Handler](https://docs.python-telegram-bot.org/en/v20.0a4/telegram.ext.messagehandler.html)
- Stands for registering messages with any types of files attached to them
- Callback function: `interfaces.telegram_event_router.router.route_event`

#### Member Handlers
Handles `chat_member` updates

##### Member Handler
- Based on [Telegram Chat Member Handler](https://docs.python-telegram-bot.org/en/v20.0a4/telegram.ext.chatmemberhandler.html)
- Stands for registering any status changes of chat members, where bot is present
- Callback function: `interfaces.telegram_event_router.router.route_event`

#### Conversation Handlers
Holds `validation` logic

##### Conversation Validation Handler
- Based on [Telegram Conversation Handler](https://docs.python-telegram-bot.org/en/v20.0a4/telegram.ext.conversationhandler.html), [Telegram Message Handler](https://docs.python-telegram-bot.org/en/v20.0a4/telegram.ext.messagehandler.html) and [Telegram Command Handler](https://docs.python-telegram-bot.org/en/v20.0a4/telegram.ext.basehandler.html)
- Responsible for new member validation procedure. Process messages separately from other handlers.
- Starting point: `/start_validation` command
- Stop: `/cancel_validation` command
- Callback: `interfaces.telegram_event_handlers.conversation_update.validator`
