sudo ps -ef | grep gunicorn | grep -v grep | awk '{print $2}' | xargs sudo kill -9
cd /home/pi/videorecorder/
sudo gunicorn  --workers=1 --threads=4 --access-logfile logs/access.log  --bind=0.0.0.0:8100 --timeout 300 wsgi:app >> logs/out.log 2>&1 &
