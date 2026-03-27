#!/bin/bash
echo "Uninstalling dzimba.."

INFRA_DIR=infra
TEMP_DIR=uninstall-temp

echo "Switching to '${INFRA_DIR}' directory.."
cd $INFRA_DIR

echo "Creating temp directory.."
mkdir $TEMP_DIR && cd $_

# bvisa basa
crontab -l | awk -v container="$DZIMBA_CONTAINER_NAME" '$0 !~ container {print}' > $DZIMBA_CRON_TMP
crontab $DZIMBA_CRON_TMP

# remove env vars from bashrc
cd ..
rm -fr $TEMP_DIR
cd ..
