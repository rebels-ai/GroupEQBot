# `GroupEQBot` 

## Prerequisites
To utilize GroupEQBot system, firstly setup `configurations.confurations.yaml` file based on `sample.yaml`, 
fulfilling bot `name`, `token`, `url` fields (refer to `System Configurations` clause), obtained while telegram creating bot process.  

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

## Deployment
To deploy GroupEQBot separately of rest of the services:
```
$ docker build . Dockerfile
$ docker run . Dockerfile 
```
