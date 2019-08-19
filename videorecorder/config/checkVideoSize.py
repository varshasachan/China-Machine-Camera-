import os

imei = open('/home/pi/videorecorder/config/IMEI', 'r').read().rstrip()

last_filesize = os.popen("ls /media/pi/" + imei + "/ -alrth -Art | tail -n 1 | awk '{print $5}'").read()

if last_filesize == '5.6K':
	os.popen("sudo ps -ef | grep gunicorn | grep -v grep | awk '{print $2}' | xargs sudo kill -9")
	os.popen('sudo sh /home/pi/videorecorder/config/rc.sh')
