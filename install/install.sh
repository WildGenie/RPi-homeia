#!/bin/sh
#-------------------------------------------------------------------
# HOMEIA installer: shell script to deploy HOMEIA and dependencies
#-------------------------------------------------------------------
echo Starting installation
echo "********************************************************"
# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi
apt-get update
apt-get install python-pip
pip install flask

#git clone https://github.com/miniupnp/miniupnp.git
#cd ~/miniupnp/miniupnpc
#make install
#make pythonmodule
#make installpythonmodule
#make clean

apt-get install miniupnpc


