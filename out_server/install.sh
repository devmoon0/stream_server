#!/bin/bash
RED='\033[0;31m'
BLUE='\033[0;34m'
BRED='\033[1;31m'
BBLUE='\033[1;34m'
NC='\033[0m'

sudo systemctl stop test_cctv8 >/dev/null 2>&1

sudo mkdir -p /opt/test_cctv8

sudo cp test_cctv8.service /etc/systemd/system/
sudo cp start_cctv8.sh /opt/test_cctv8

sudo chmod 755 /opt/test_cctv8/start_cctv8.sh

sudo systemctl daemon-reload
sudo systemctl start test_cctv8
if [[ "$?" != "0" ]]; then
	echo -e "${BRED}ERROR: fail to start test_cctv8 service${NC}"
	sudo systemctl status test_cctv8
	exit -1
fi
echo -e "${BBLUE}installation complete${NC}"