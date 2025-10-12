#!/bin/bash

container=`docker ps -a | awk '/house_finder/ {print $NF}'`
if [ "$container" != "$DZIMBA_CONTAINER_NAME" ]; then
	echo "No existing container found."
	echo "Creating container.."
	cd infra
	./setup.sh $DZIMBA_IMAGE_NAME $DZIMBA_CONTAINER_NAME
	cd ..
	
	echo "Adding cron job.."
	touch current_tabs.txt
	crontab -l > current_tabs.txt
	echo "DZIMBA_CONTAINER_NAME=$DZIMBA_CONTAINER_NAME" >> current_tabs.txt
	echo "0-59/15 * * * * sh $PWD/dzimba.sh" >> current_tabs.txt
        crontab current_tabs.txt
        rm current_tabs.txt	
fi	

docker start $DZIMBA_CONTAINER_NAME
echo "Tapedza basa.."
