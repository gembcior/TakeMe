#!/bin/bash

DOCKER_COMPOSE_NAME=$(docker compose ps -a | cut -d ' ' -f1 | head -2 | tail -1)
echo "Backup for ${DOCKER_COMPOSE_NAME}"
mkdir -p backup
docker run --rm --volumes-from ${DOCKER_COMPOSE_NAME} -v $(pwd)/backup:/backup --env-file application.env takeme tar -cvf /backup/backup-$(date +"%Y-%m-%d").tar .
echo "Backup done for ${DOCKER_COMPOSE_NAME}"
