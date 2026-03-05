# temporary file to store current tabs
temp_file="current_tabs"
touch $temp_file

# remove any lines in the cron table
# related to this project
crontab -l | awk -v prefix="$DZIMBA_CONTAINER_NAME" '$0 !~ prefix {print}' > $temp_file

# add new job to temp file
# set new file as new cron table
# remove temporary file
echo "0-59/5 * * * * docker start -i $DZIMBA_CONTAINER_NAME >> $PWD/logs.txt 2>&1" >> $temp_file
crontab $temp_file
rm $temp_file
