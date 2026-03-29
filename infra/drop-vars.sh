#!/bin/bash

echo "Removing env vars associated with dzimba.."
cp ~/.bashrc ~/$FALLBACK_BASHRC
cat ~/.bashrc | awk '$0 !~ /DZIMBA/ {print}' > $TEMP_BASHRC
truncate -s -2 $TEMP_BASHRC
cat $TEMP_BASHRC > ~/.bashrc
source ~/.bashrc
