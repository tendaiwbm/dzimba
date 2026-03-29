#!/bin/bash
echo "Uninstalling dzimba.."

INFRA_DIR=infra
TEMP_PURGE_DIR=uninstall-temp

echo "Switching to '${INFRA_DIR}' directory.."
cd $INFRA_DIR

# container nemufananidzi ngazviende
echo "Purging docker infra.."
./remove.sh

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
