# Event Processors
Private and Public processors are responsible for handling validated Telegram events based on EventType

## Private Processors
* General `PrivateProcessor` for now handles only BOT events and directs them to BotEventProcessor
    * `BotEventProcessor` is responsible for handling changes in bot status, which can occur in 1:1 chats (user : bot)

## Public Processors
* General PublicProcessor handles MESSAGE, MEMBER and BOT events and directs them to following processors:
    * `BotEventProcessor` is responsible for handling changes in bot status, which can occur in group chats where bot is located
    * `MemberEventProcessor` handles any status changes of chat members, where bot `GroupEQBot` is an admin
    * `MessageEventProcessor` handles any message events regardles of content type of that message