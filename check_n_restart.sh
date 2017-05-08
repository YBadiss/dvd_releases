#!/bin/sh

FILE="/home/ubuntu/.restart"

if [ -f "$FILE" ]
then
    echo "Pulling and restarting"
    rm -f $FILE

    sudo rm -rf /home/ubuntu/dvd_releases
    git clone https://github.com/YBadiss/dvd_releases.git /home/ubuntu/dvd_releases

    sudo cp /home/ubuntu/dvd_releases/configs/supervisord.conf /etc/supervisord.conf
    crontab < /home/ubuntu/dvd_releases/configs/crontab

    /usr/local/bin/supervisorctl reread
    /usr/local/bin/supervisorctl restart all
else
    echo "File $FILE does not exist, nothing to be done"
fi
