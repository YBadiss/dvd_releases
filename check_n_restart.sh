#!/bin/sh

FILE="/home/ubuntu/.restart"

if [ -f "$FILE" ]
then
    echo "Pulling and restarting"
    rm -f $FILE

    cd /home/ubuntu
    rm -rf dvd_releases
    git clone https://github.com/YBadiss/dvd_releases.git

    cd dvd_releases
    sudo cp configs/supervisord.conf /etc/supervisord.conf
    crontab < configs/crontab

    /usr/local/bin/supervisorctl reread
    /usr/local/bin/supervisorctl restart all
else
    echo "File $FILE does not exist, nothing to be done"
fi
