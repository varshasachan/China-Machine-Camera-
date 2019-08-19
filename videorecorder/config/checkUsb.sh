#!/bin/sh
imei=`cat /home/pi/videorecorder/config/IMEI`
echo "$imei"
command=`df -h | grep /dev/sd[a-z]`
if [ $? != 0 ]; 
then
    echo USB not connected
    curl "https://prod-api.tinymart.in/email/sendAlert?imei="$imei"&message=USB_not_connected"
else
    echo USB connected
    command1=`df -h | grep /dev/sd[a-z] | awk '{ print $2 }'`
    echo $command1

    command2=`df -h | grep /dev/sd[a-z] | awk '{ print $5 }'`
    echo ${command2%\%}
    if [ ${command2%\%} -gt 80 ];
    then
	echo Memory full
        curl "https://prod-api.tinymart.in/email/sendAlert?imei="$imei"&message=USB_memory_full"
    else
	echo good to go
    fi
fi


