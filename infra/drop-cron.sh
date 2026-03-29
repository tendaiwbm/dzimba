#!/bin/bash

echo "Basa rakubviswa.."
crontab -l | awk -v container="$DZIMBA_CONTAINER_NAME" '$0 !~ container {print}' > $DZIMBA_CRON_TMP
crontab $DZIMBA_CRON_TMP

rm $DZIMBA_CRON_TMP
