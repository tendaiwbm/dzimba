# remove existing cron
# code comes here

touch current_tabs.txt
crontab -l > current_tabs.txt
echo "DZIMBA_CONTAINER_NAME=$DZIMBA_CONTAINER_NAME" >> current_tabs.txt
echo "0-59/5 * * * * docker start $DZIMBA_CONTAINER_NAME >> logs.txt 2>&1" >> current_tabs.txt
crontab current_tabs.txt
rm current_tabs.txt
