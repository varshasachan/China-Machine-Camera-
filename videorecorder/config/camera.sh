#!/bin/bash
imei=`cat /home/pi/videorecorder/config/IMEI`
echo "$imei"
command=`ls /dev/video*`
if [ $? != 0 ]; 
then
    echo camera not connected
    curl "https://prod-api.tinymart.in/email/sendAlert?imei="$imei"&message=camera_not_connected"
else
    echo camera connected
fi


