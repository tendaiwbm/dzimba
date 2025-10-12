#!/bin/bash

./remove.sh $1 $2
docker build -t $1 -f Dockerfile .
docker create --name $2 --mount type=bind,source=..,target=/app -p 8085:8085 $1
