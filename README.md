## Introduction
To make your version of `GroupEQBot`, firstly you have to create your own bot in Telegram 
and apply changes in `source.group_eq_bot.configurations` accordingly.   

## Bot Creation
Navigate to [BotFather](https://telegram.me/BotFather) and apply following steps:

1. Use command `/newbot`
   - Create a name for your bot

2. Create a username, which must ends with 'bot' (it would be used as `url` to bot)
   - ``` example: "t.me/name_of_your_bot" ```
   
3. Use command `/setprivacy` and choose `Disable` 
4. Use `/setdescription` command to make bot description 
5. Use `/setcommands` command to create `2 validation commands`:
   - `start_validation` - command which initiates validation process
   - `cancel_validation` - command which cancels validation process 
   
6. Fulfill bot name, bot token, bot url in `configurations.yaml` file

## Licence
[Rebels.AI](https://rebels.ai) has made this service available for you to incorporate into your products under the [MIT Licence](https://mit-license.org). Feel free to remix and re-share the service and documentation in your products.
[Rebels.AI](https://rebels.ai)'d love attribution in your usecases *about* telegram bots, but it's not required.
