## System Deployment
#### To deploy all services:
```bash
$ docker-compose up --build --force-recreate
```

#### To deploy particular profile (service):
```bash
$ docker compose --profile {profileName} up --build --force-recreate

* Wilth single profile
$ docker compose --profile server up --build --force-recreate
  
* Wilth multiple profiles
$ docker compose --profile server --profile database up --build --force-recreate 
```

# Database & GroupEQBot
After deploying database and GroupEQBot you have to get following:
```
CONTAINER ID   IMAGE                                                  COMMAND                  CREATED         STATUS         PORTS                              NAMES
0442b0d14ee6   docker.elastic.co/kibana/kibana:7.4.0                  "/usr/local/bin/dumb…"   2 minutes ago   Up 2 minutes   0.0.0.0:5601->5601/tcp             events-storage-manager
71394b28d18b   docker.elastic.co/elasticsearch/elasticsearch:7.10.2   "/tini -- /usr/local…"   2 minutes ago   Up 2 minutes   0.0.0.0:9200->9200/tcp, 9300/tcp   events-storage
9498f9913f2e   group-eq-bot:1.0.0                                     "python ./run_bot.py"    2 minutes ago   Up 2 minutes                                      group-eq-bot
```

- Container `events-storage-manager` - stands for UI to navigate the data (Kibana)
- Container `events-storage` - stands for persistent storage (Elasticsearch)
- Container `group-eq-bot` - stands for bot functionalities