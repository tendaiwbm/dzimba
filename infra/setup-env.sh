#!/bin/bash

./remove-docker-infra.sh
docker build --no-cache -t $DZIMBA_IMAGE_NAME -f Dockerfile .
docker create --name $DZIMBA_CONTAINER_NAME --mount type=bind,source=..,target=/app -p 8085:8085 $DZIMBA_IMAGE_NAME
