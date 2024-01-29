#!/bin/bash

echo "Backup"
mkdir -p backup
docker compose run --rm -v $(pwd)/backup:/backup takeme tar -cvf /backup/backup-$(date +"%Y-%m-%d-%H-%M").tar .
echo "Backup done"
