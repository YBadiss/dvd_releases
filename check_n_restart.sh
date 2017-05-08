#!/bin/sh

FILE="/home/ubuntu/.restart"

cd /home/ubuntu/dvd_releases/

if [ -f "$FILE" ]
then
    echo "Pulling and restarting"
    rm -f $FILE
    git pull
    sudo cp configs/supervisord.conf /etc/supervisord.conf
    crontab < configs/crontab
    supervisorctl reread
    supervisorctl restart all
fi