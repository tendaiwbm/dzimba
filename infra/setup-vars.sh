#!/bin/bash
task_dir="setup-dir"

# create dir to setup env variables
echo "Creating temp directory '$task_dir'.."
mkdir $task_dir
echo "Switching to temp directory '$task_dir'.."
cd $task_dir

# copy user bashrc before attempting to update
cat ~/.bashrc > $FALLBACK_BASHRC

# replace existing/put in place project variables
awk '$0 !~ /DZIMBA/{print}' $FALLBACK_BASHRC >> $TEMP_BASHRC
truncate -s -1 $TEMP_BASHRC

echo -e "\n# DZIMBA vars" >> $TEMP_BASHRC
for line in `cat ../.env`;
do
	echo "export $line" >> $TEMP_BASHRC 	
done
echo -e "\n" >> $TEMP_BASHRC

mv $TEMP_BASHRC ~/.bashrc
source ~/.bashrc

# cleaning up
echo "Cleaning up.."
cd ..
rm -rf $task_dir
