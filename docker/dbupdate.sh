#!/bin/bash

echo "Update database"
docker compose run --rm takeme flask --app takeme db migrate
docker compose run --rm takeme flask --app takeme db upgrade
echo "Update database done"
