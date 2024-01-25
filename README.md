# Development
## Introduction
Project is using `poetry` to manage dependencies.

## How To Run Development Server
```
poetry run python -m takeme.run
```

# Deploy
## Introduction
Project is using docker compose plugin to deploy application on production server. Run all following comands from the `docker` directory.

## Deploy new application instance
```
docker compose up -d
```

## Stop the application
```
docker compose stop
```

## Start the application
```
docker compose stop
```

# Backup
## Introduction
Project is using docker volumes to store database file. This allow to retain database even after application container will be killed.

## Do a backup
```
./backup.sh
```

# Database Update
