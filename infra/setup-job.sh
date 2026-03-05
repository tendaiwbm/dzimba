# temporary file to store current tabs
touch $DZIMBA_CRON_TMP

# remove any lines in the cron table
# related to this project
crontab -l | awk -v prefix="$DZIMBA_CONTAINER_NAME" '$0 !~ prefix {print}' > $DZIMBA_CRON_TMP

# add new job to temp file
# set new file as new cron table
# remove temporary file
echo "0-59/5 * * * * docker start -i $DZIMBA_CONTAINER_NAME >> $PWD/$DZIMBA_APP_LOGFILE 2>&1" >> $DZIMBA_CRON_TMP
crontab $DZIMBA_CRON_TMP
rm $DZIMBA_CRON_TMP
