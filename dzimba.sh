#======================================================#
#                  Copyright © 2026                    #
#                                                      #
#  This is an installation script for the Dzimba app.  #
#                                                      #
#               Author: Tendai Mbwanda                 #
#             Email: tmbwanda52@gmail.com              #
#======================================================#

INFRA_DIR=infra

if [ -z "${DZIMBA_VARIABLES_INSTALLED}" ]; then
	echo "Setting up environment variables.."
	
	cd $INFRA_DIR
	source setup-vars.sh
	cd ..
fi

job=`crontab -l | awk -v string="$DZIMBA_CONTAINER_NAME" '$0 ~ string {print}'`
container=`docker ps -a | awk -v string="$DZIMBA_CONTAINER_NAME" '$0 ~ string {print $NF}'`

if [ -z "${job}" ]; then
	cd $INFRA_DIR

	if [ -z "$container" ]; then
		echo "Container rashaikwa.."
		
		echo "Image ne container zvakugadzigwa.."
		./setup-env.sh
		
		echo "Mufananidzo ne container zvavepo.."
	else
		echo "Docker container riripo nechekare.."
	fi

	echo "Adding cron job.."
	sh setup-job.sh
	
	cd ..
fi	

echo "Tapedza basa!"
