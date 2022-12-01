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