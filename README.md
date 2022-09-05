# Telegram `GroupEQBot` 

## Motivation
Nowadays, a buzzy request of any `telegram group` **owner/administrator** is to have a tool, which allows `detecting 
toxic (spamming/harming) group members`, leading to way more accurate and efficient `process of moderating the groups` to enchance EQ and grow social capital of the chat groups. 

Generally it is not only about filtering toxic people and toxic comments, it is about seeking mutual interests, and adding juce to communication, performing things like random coffe matching of persons potentially interesting for each other. Whois coffee bot is meant to encouraging people to leave their traditional circle of cummunication and learn new things.

Based on experience of [Rebels.AI](https://rebels.ai) in solving ML problems on daily bases, notably in NLP, 
strongly believe that solve substantial chatting-related problems, making the communication
more `ethical`, `secured`, `targeted` and in general, `wholesome` is a right thing to do.


## Technical Description
Mainly, `GroupEQBot` bot service stands for: 
- `validating users`, who aiming to join [telegram group](https://www.telegram-group.com/en/blog/the-difference-between-telegram-groups-and-telegram-channels/) 
- `capturing and analyzing users behaviour` within [telegram group](https://www.telegram-group.com/en/blog/the-difference-between-telegram-groups-and-telegram-channels/)  
- `providing analytics` per [telegram group](https://www.telegram-group.com/en/blog/the-difference-between-telegram-groups-and-telegram-channels/) per user
- `based on employed clustering and classification` ML algorithms, detect suspicious users and contrary, unite users with common interests 


## System Design Overview
``
Note: system design can vary during development process. 
``
![WICB_system_design_overview](https://user-images.githubusercontent.com/97040130/178306103-26cbb0b6-fe38-407c-be79-9434fec6db33.jpg)


## System Deployment
``
From the "source" folder, invoke:
``
```bash
$ docker-compose up --build --force-recreate
```

## Demo Example
#### New member attempts to pass the validation

`Member passed validation`

https://user-images.githubusercontent.com/37558223/185430821-7f63f561-2e57-453f-b44f-a815348fcf92.mp4

`Member failed validation`

https://user-images.githubusercontent.com/37558223/185430839-3f5d6fc0-92b7-47c0-b134-a6cdcf6a380a.mp4


## Licence
[Rebels.AI](https://rebels.ai) has made this service available for you to incorporate into your products under the [MIT Licence](https://mit-license.org). Feel free to remix and re-share the service and documentation in your products.
[Rebels.AI](https://rebels.ai)'d love attribution in your usecases *about* telegram bots, but it's not required.
