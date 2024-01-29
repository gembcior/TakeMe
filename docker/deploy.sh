#!/bin/bash

echo "Deploy TakeMe app"
docker compose run --rm takeme flask --app takeme db init
docker compose up -d
echo "Deploy TakeMe app done"
