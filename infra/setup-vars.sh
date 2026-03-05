echo "Setting up variables.."

task_dir="setup-dir"
bashrc1="bashrc_backup"
bashrc2="bashrc_temp"

# create dir to setup env variables
echo "Creating temp directory '$task_dir'.."
mkdir $task_dir
echo "Switching to temp directory '$task_dir'.."
cd $task_dir

# copy user bashrc before attempting to update
touch $bashrc1
touch $bashrc2
cat ~/.bashrc > $bashrc1
cp $bashrc1 ~/$bashrc1

# replace existing/put in place project variables
awk '$0 !~ /DZIMBA/{print}' $bashrc1 >> $bashrc2
truncate -s -1 $bashrc2

echo -e "\n# DZIMBA vars" >> $bashrc2
for line in `cat ../.env`;
do
	echo "export $line" >> $bashrc2 	
done

mv $bashrc2 ~/.bashrc
source ~/.bashrc

# cleaning up
echo "Cleaning up.."
cd ..
rm -rf $task_dir

echo "Tapedza basa!"
