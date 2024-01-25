#!/bin/bash

DOCKER_COMPOSE_NAME=$(docker compose ps | cut -d ' ' -f1 | head -2 | tail -1)
echo "Backup for ${DOCKER_COMPOSE_NAME}"
mkdir -P backup
docker run --rm --volumes-from ${DOCKER_COMPOSE_NAME} -v $(pwd)/backup:/backup ubuntu tar cvf /backup/backup-$(date +"%Y-%m-%d").tar /usr/var/takeme-instance
echo "Backup done for ${DOCKER_COMPOSE_NAME}"
