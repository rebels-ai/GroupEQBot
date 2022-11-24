# GroupEQBot Handlers:

GroupEQBot handlers are the wrapper on top of native [Telegram Handlers](https://docs.python-telegram-bot.org/en/v20.0a4/telegram.ext.handlers-tree.html).

There are following internal `handlers` types:
  - member_update
  - message_update
    - audio
    - video
    - text
    - document
  - conversation_update
 

## GroupEQBot Handler Sample Interface
Any of the GroupEQBot handlers interface are declared as:
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


## GroupEQBot Available Handlers (by types)

### message_update
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
- Stands for registering messages. containing any types of files
- Callback function: `interfaces.telegram_event_router.router.route_event`

### member_update
##### Member Handler
- Based on [Telegram Chat Member Handler](https://docs.python-telegram-bot.org/en/v20.0a4/telegram.ext.chatmemberhandler.html)
- Stands for registering any chat member status change
- Callback function: `interfaces.telegram_event_router.router.route_event`

##### Bot Handler
- Based on [Telegram Chat Member Handler](https://docs.python-telegram-bot.org/en/v20.0a4/telegram.ext.chatmemberhandler.html)
- Stands for registering any bot status change
- Callback function: `interfaces.telegram_event_router.router.route_event`

### conversation_update
##### Conversation Validation Handler
- Based on:
  - [Telegram Conversation Handler](https://docs.python-telegram-bot.org/en/v20.0a4/telegram.ext.conversationhandler.html)
  - [Telegram Callback Query Handler](https://docs.python-telegram-bot.org/en/v20.0a4/telegram.ext.callbackqueryhandler.html)
  - [Telegram Message Handler](https://docs.python-telegram-bot.org/en/v20.0a4/telegram.ext.messagehandler.html)
  - [Telegram Command Handler](https://docs.python-telegram-bot.org/en/v20.0a4/telegram.ext.basehandler.html)
- Responsible for new member validation process. Process messages separately from other handlers.
- Initial check: `/start_validation` command
- Entrypoint: `interfaces.telegram_event_handlers.conversation_update.button`
- Stop: `/cancel_validation` command
- Callback: `interfaces.telegram_event_handlers.conversation_update.constructor`