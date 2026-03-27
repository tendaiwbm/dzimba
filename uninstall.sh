#!/bin/bash
echo "Uninstalling dzimba.."

INFRA_DIR=infra
TEMP_DIR=uninstall-temp
TEMP_BASHRC=bashrc_temp

echo "Switching to '${INFRA_DIR}' directory.."
cd $INFRA_DIR

# container nemufananidzi ngazviende
echo "Purging docker infra.."
./remove.sh

echo "Creating temp directory.."
mkdir $TEMP_DIR && cd $_

# bvisa basa
echo "Basa rakubviswa.."
crontab -l | awk -v container="$DZIMBA_CONTAINER_NAME" '$0 !~ container {print}' > $DZIMBA_CRON_TMP
crontab $DZIMBA_CRON_TMP

# remove env vars from bashrc
echo "Removing env vars associated with dzimba.."
cat ~/.bashrc | awk '$0 !~ /DZIMBA/ {print}' > $TEMP_BASHRC
truncate -s -2 $TEMP_BASHRC
cat $TEMP_BASHRC > ~/.bashrc
source $TEMP_BASHRC

echo "Takutsvaira.."
cd ..
rm -fr $TEMP_DIR
cd ..
