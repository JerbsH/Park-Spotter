#!/bin/bash
# Update and upgrade system packages
sudo apt-get update -y
sudo apt-get upgrade -y

# Install pip
sudo apt-get install python-pip -y

# Install pm2
sudo apt-get install nodejs -y
sudo apt-get install npm -y
sudo npm install pm2 -g

# Get newest version
git pull origin main

# Install required python packages
pip install -r ./backend/requirements.txt

# Run the Flask server with PM2
pm2 start ./backend/flaskserver.py --name=flaskserver --interpreter python3

# Run the other script with PM2
pm2 start ./backend/streamyolo.py --name=parkspotter --interpreter python3



