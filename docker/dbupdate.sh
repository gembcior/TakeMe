#!/bin/bash

DOCKER_COMPOSE_NAME=$(docker compose ps -a | cut -d ' ' -f1 | head -2 | tail -1)
echo "Update database for ${DOCKER_COMPOSE_NAME}"
docker run --rm --volumes-from ${DOCKER_COMPOSE_NAME} --env-file application.env takeme flask --app takeme db migrate
docker run --rm --volumes-from ${DOCKER_COMPOSE_NAME} --env-file application.env takeme flask --app takeme db upgrade
echo "Update database done for ${DOCKER_COMPOSE_NAME}"
