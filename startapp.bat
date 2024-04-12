@echo off
cd /d %~dp0

:: Install pm2
:: You need to have Node.js and npm installed in Windows
npm install pm2 -g

:: Get newest version
git pull origin main

:: Install required python packages
python -m pip install -r ./backend/requirements.txt

:: Run the Flask server in the background
pm2 start ./backend/flaskserver.py --name flaskserver --interpreter python

:: Run the Flask server in the background
pm2 start ./backend/streamyolo.py --name parkspotter --interpreter python
