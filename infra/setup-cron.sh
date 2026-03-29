#!/bin/bash

# remove any existing jobs for dzimba
./drop-cron.sh

# add new job to temp file
# set new file as new cron table
# remove temporary file
echo "0-59/5 * * * * docker start -i $DZIMBA_CONTAINER_NAME >> $PWD/$DZIMBA_APP_LOGFILE 2>&1" >> $DZIMBA_CRON_TMP
crontab $DZIMBA_CRON_TMP

rm $DZIMBA_CRON_TMP
