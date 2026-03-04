#======================================================#
#                  Copyright © 2026                    #
#                                                      #
#  This is an installation script for the Dzimba app.  #
#                                                      #
#  If no  existing docker container for this project   #
#  is found, the following happens                     #
#  1. Adding the project environment variables         #
#     to ~./bashrc.                                    #
#  2. A clean docker image build and container setup.  #
#  3. Installation of a cron job that runs             #
#     the Dzimba bot.                                  #
#                                                      #
#               Author: Tendai Mbwanda                 #
#             Email: tmbwanda52@gmail.com              #
#======================================================#

container=`docker ps -a | awk '/house_finder/ {print $NF}'`

if [ "$container" != "$DZIMBA_CONTAINER_NAME" ]; then
	echo "Container rashaikwa.."
	
	echo "Setting up environment variables.."
	cd infra
	source setup-vars.sh
	
	echo "Image ne container zvakugadzigwa.."
	./setup-env.sh
	
	echo "Finished creating image & container.."
	
	echo "Adding cron job.."
	sh setup-job.sh

	cd ..
else
	echo "Setup skipped, docker container riripo nechekare.."
fi	

echo "Tapedza basa!"
