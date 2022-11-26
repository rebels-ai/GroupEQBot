## Bot creation
To create a bot on Telegram, you need to contact the [BotFather](https://telegram.me/BotFather) and go through the following steps:
1. Use command `/newbot`
2. Create a name for your bot
3. Create a username, which must ends with 'bot'. It would be used as a url to bot

    e.g.: `t.me/name_of_your_bot`
4. Set privacy with command `/setprivacy` to `Disable`, so bot receive all messages that people send in group chats
5. Put bot token you received to `token` field in `configurations.yaml` (see system configurations further in README.md)

In BotFather's chat you can set other useful bot features as well:
- With `/setdescription` command you can change bot description, which is shown when users open private chat with bot
- `/setcommands` can be used to set bot menu in reply box for easier access to your bot commands

## System Deployment
``
If you would like to deploy all services:
``

```bash
$ docker-compose up --build --force-recreate
```

``
If you would like to deploy particular profile (sevice):
``

```bash
$ docker compose --profile {profileName} up --build --force-recreate 
```
```bash
e.g.: $ docker compose --profile server up --build --force-recreate
or wilth multiple profiles
e.g.: $ docker compose --profile server --profile database up --build --force-recreate
```

events-storage: localhost:9200
events-storage-manager: localhost:5601

## Licence
[Rebels.AI](https://rebels.ai) has made this service available for you to incorporate into your products under the [MIT Licence](https://mit-license.org). Feel free to remix and re-share the service and documentation in your products.
[Rebels.AI](https://rebels.ai)'d love attribution in your usecases *about* telegram bots, but it's not required.
