# Telegram `GroupEQBot` 
Registered telegram bot can be found in telegram passing `@GroupEQBot` in search bar.


## Motivation
Nowadays, a buzzy request of any `telegram group` **owner/administrator** is to have a tool, which allows `detecting 
toxic (spamming/harming) group members`, leading to way more accurate and efficient `process of moderating the groups` to enchance EQ and grow social capital of the chat groups. 

Generally it is not only about filtering toxic people and toxic comments, it is about seeking mutual interests, and adding juce to communication, performing things like random coffe matching of persons potentially interesting for each other. Whois coffee bot is meant to encouraging people to leave their traditional circle of cummunication and learn new things.

Based on experience of [Rebels.AI](https://rebels.ai) in solving ML problems on daily bases, notably in NLP, 
strongly believe that solve substantial chatting-related problems, making the communication
more `ethical`, `secured`, `targeted` and in general, `wholesome` is a right thing to do.


## Technical Description
- Mainly, `GroupEQBot` bot service stands for:
  - registering & validating & transforming & ingesting incoming Telegram group(S) events    
  - `validating users`, who aiming to join [telegram group](https://www.telegram-group.com/en/blog/the-difference-between-telegram-groups-and-telegram-channels/) 
  - `capturing and analyzing users behaviour` within [telegram group](https://www.telegram-group.com/en/blog/the-difference-between-telegram-groups-and-telegram-channels/)  
  - `providing analytics` per [telegram group](https://www.telegram-group.com/en/blog/the-difference-between-telegram-groups-and-telegram-channels/) per user
  - `based on employed clustering and classification` ML algorithms, detect suspicious users and contrary, unite users with common interests

- Registered by `GroupEQBot` Telegram groups events are ingested in and managed with:
  - ElasticSearch (stands for storing `events`, `users` and `groups` data)
  - Kibana (stands for UI to manage | query | visualise `events`, `users` and `groups` data)

## System Design ![Screenshot 2022-10-09 at 18 05 02](https://user-images.githubusercontent.com/37558223/194764215-3d3584b9-b28b-4283-9d2c-44efee6db278.png)

## Bot creation
To create a bot on Telegram, you need to contact the [BotFather](https://telegram.me/BotFather) and go through the following steps:
1. Use command `/newbot`
2. Create a name for your bot
3. Create a username, which must ends with 'bot'. It would be used as a url to bot

    e.g.: `t.me/name_of_your_bot`
4. Set privacy with command `/setprivacy` to `Disable`, so bot receive all messages that people send in group chats
5. Put bot token you received to `token` field in `configurations.yaml`

In BotFather's chat you can set bot profile picture, description, commands and delete the bot as well.

## System Configurations
- There is configurations template file, containing all the system configurations:
```
group_eq_bot/configurations/sample.yaml
```

To set up the system before deploying, navigate to the configurations folder:
 - `copy` `sample.yaml` and name it `configuration.yaml`
```bash
$ mv sample.yaml configuration.yaml
```
 - `fill` `configuration.yaml`
```bash
$ nano configuration.yaml
```

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


## Licence
[Rebels.AI](https://rebels.ai) has made this service available for you to incorporate into your products under the [MIT Licence](https://mit-license.org). Feel free to remix and re-share the service and documentation in your products.
[Rebels.AI](https://rebels.ai)'d love attribution in your usecases *about* telegram bots, but it's not required.
