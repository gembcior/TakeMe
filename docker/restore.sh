#!/bin/bash

BACKUP=$1
DOCKER_COMPOSE_NAME=$(docker compose ps -a | cut -d ' ' -f1 | head -2 | tail -1)
echo "Restore backup ${BACKUP} for ${DOCKER_COMPOSE_NAME}"
docker run --rm --volumes-from ${DOCKER_COMPOSE_NAME} -v $(pwd)/backup:/backup --env-file application.env takeme tar -xvf /backup/${BACKUP} --wildcards *db.sqlite
echo "Restore backup ${BACKUP} for ${DOCKER_COMPOSE_NAME} done"
