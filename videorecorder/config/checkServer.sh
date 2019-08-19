#!/usr/bin/env bash
ping_url="localhost:8100/ping"
ping_status=`curl -s -o /dev/null -w "%{http_code}\n" $ping_url`

if [ "$ping_status" = "200" ]; then
    echo "---- Ping successful."
else
    echo "Killing gunicorn"
    sudo ps -ef | grep gunicorn | grep -v grep | awk '{print $2}' | xargs sudo kill -9
    echo "Starting gunicorn"
    cd /home/pi/videorecorder/
    sudo gunicorn --workers=1 --threads=4 --access-logfile logs/access.log  --bind=0.0.0.0:8100 --timeout 300 wsgi:app >> logs/out.log 2>&1 &

    sleep 5 

    ping_status=`curl -s -o /dev/null -w "%{http_code}\n" $ping_url`
    if [ "$ping_status" = "200" ]; then
        echo "---- Ping successful."
    else
        echo "---- Error starting gunicorn. Please check."
    fi
fi

