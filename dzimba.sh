#!/bin/bash

container=`docker ps -a | awk '/house_finder/ {print $NF}'`

if [ "$container" != "$DZIMBA_CONTAINER_NAME" ]; then
	echo "Container rashaikwa.."
	echo "Image ne container zvakugadzigwa.."
	
	cd infra
	./setup.sh $DZIMBA_IMAGE_NAME $DZIMBA_CONTAINER_NAME
	
	echo "Finished creating container.."
	
	cd ..
	
	echo "Adding cron job.."
	sh install_cron.sh $DZIMBA_CONTAINER_NAME
else
	echo "Setup skipped, docker container riripo nechekare.."
fi	

echo "Tapedza basa!"
