#!/bin/bash
# Update and upgrade system packages
sudo apt-get update -y
sudo apt-get upgrade -y

# Install pip
sudo apt-get install python3-pip -y

# Install pm2
sudo apt-get install nodejs -y
sudo apt-get install npm -y
sudo npm install pm2 -g

# Install required python packages
pip install -r ./backend/requirements.txt

# Run the Flask server in the background
yes | python3 ./backend/flaskserver.py &

# Run the Flask server in the background
pm2 start ./backend/streamyolo.py --name=parkspotter --interpreter python3

