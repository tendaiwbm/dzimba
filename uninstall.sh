#!/bin/bash
echo "Uninstalling dzimba.."

INFRA_DIR=infra
TEMP_PURGE_DIR=uninstall-temp

echo "Switching to '${INFRA_DIR}' directory.."
cd $INFRA_DIR

# container nemufananidzi ngazviende
echo "Purging docker infra.."
./remove-docker-infra.sh

# bvisa basa
./drop-cron.sh

echo "Creating temp directory.."
mkdir $TEMP_PURGE_DIR && cd $_

# remove env vars from bashrc
source ../drop-vars.sh

echo "Takutsvaira.."
cd ..
rm -fr $TEMP_PURGE_DIR
cd ..

drop_project_files=""
while getopts "r:" flag; do
    case "${flag}" in
	    r) drop_project_files="true" ;;
    esac
done

if [ ! -z "$drop_project_files" ]; then
	root_dir=$PWD
	cd ..
	yes | rm -rf $root_dir
fi

drop_project_files=""
