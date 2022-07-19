#!/bin/bash
RED='\033[0;31m'
BLUE='\033[0;34m'
BRED='\033[1;31m'
BBLUE='\033[1;34m'
NC='\033[0m'

sudo mkdir -p /opt/test_cctv8
sudo cp start_server.sh call_server.sh /opt/test_cctv8/

sudo chmod 755 /opt/test_cctv8/start_server.sh
sudo chmod 755 /opt/test_cctv8/call_server.sh

sudo cp cctv8_server.service  call_server.service /etc/systemd/system

sudo systemctl daemon-reload

sudo systemctl start call_server
sudo systemctl status call_server
sudo systemctl start start_server

sudo systemctl start cctv8_server.service
sudo systemctl status cctv8_server.service

sudo systemctl restart call_server

sudo journalctl -lf -u cctv8_server
