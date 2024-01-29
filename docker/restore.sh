#!/bin/bash

BACKUP=$1

if [[ ! -f $(pwd)/backup/${BACKUP} ]]; then
  echo "ERROR: There is no ${BACKUP}"
  exit 255
fi

echo "Restore backup ${BACKUP}"
docker compose stop
docker compose run --rm -v $(pwd)/backup:/backup takeme tar -xvf /backup/${BACKUP}
docker compose start
echo "Restore backup ${BACKUP} done"
