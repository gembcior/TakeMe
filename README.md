# Development
## Introduction
Project is using `poetry` to manage dependencies.
See [poetry docs](https://python-poetry.org/docs/) how to develop with `poetry`.

## How To Run Development Server
Run following command to start development server.
```
poetry run python -m takeme.run
```

Server is than available on:
```
localhost:5000
```

# Deploy
## Introduction
The project uses the docker compose plugin to deploy the application to a production server. Execute all of the following commands from the `docker` directory.

## Deploy new application instance
```
./deploy.sh
```

## Stop the application
```
docker compose stop
```

## Start the application
```
docker compose start
```

## Kill the application
```
docker compose down
```

## Update the application
Stop current docker compose
```
docker compose stop
```

Update local repository
```
git pull
```

Rebuild docker image
```
docker compose build --no-cache
```

Update database model if required
```
./dbupdate.sh
```

Re-run the docker compose
```
docker compose up --force-recreate -d
```

# Backup
## Introduction
The project uses docker volumes to store database file. This allows to retain database even after application container is killed. Execute all of the following commands from the `docker` directory.

## Do a backup
```
./backup.sh
```

## Restore backup
```
./restore.sh <BACKUP_TAR_FILE>
```

# Database Update
## Introduction
Sometimes during development existing database model has to be changes. This require to migrate current production database file to new model.
The project is using [flask-migrate]() to handles SQLAlchemy database migrations.

## How to migrate database
### Development
Create migration entry
```
poetry run flask --app takeme db migrate -m "Message"
```

Upgrade database
```
poetry run flask --app takeme db upgrade
```

### Production
Upgrade database
```
./dbupdate.sh
```
