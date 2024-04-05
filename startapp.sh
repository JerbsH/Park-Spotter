#!/bin/bash
# Update and upgrade system packages
sudo apt-get update -y
sudo apt-get upgrade -y

# Install pip
sudo apt-get install python3-pip -y

# Install required python packages
pip install -r ./backend/requirements.txt

# Run the application
python3 ./backend/streamyolo.py