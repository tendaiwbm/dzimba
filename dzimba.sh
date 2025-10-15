#!/bin/bash

container=`docker ps -a | awk '/house_finder/ {print $NF}'`
if [ "$container" != "$DZIMBA_CONTAINER_NAME" ]; then
	echo "No existing container found."
	echo "Creating container.."
	cd infra
	./setup.sh $DZIMBA_IMAGE_NAME $DZIMBA_CONTAINER_NAME
	echo "Finished creating container."
	cd ..
	
	echo "Adding cron job.."
	sh createjob $DZIMBA_CONTAINER_NAME
fi	

docker start $DZIMBA_CONTAINER_NAME
echo "Tapedza basa.."
