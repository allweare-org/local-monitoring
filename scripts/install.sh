#!/bin/bash

echo "Installing Inverter Monitoring System..."

# update system
sudo apt update && sudo apt upgrade -y

# install python deps
sudo apt install -y python3 python3-venv python3-pip

# go to project directory
cd ~/local-monitoring/client

# create venv
python3 -m venv venv
source venv/bin/activate

# install requirements
pip install pyyaml pysolarmanv5

echo "Installation complete."
