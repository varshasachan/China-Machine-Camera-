# Camera pi module

### Order Video Recording
#### 1. Writes video in .avi format with FMP4 at 10fps
  1. `Endpoint: {cam_ip}:8100/startCam?order_id={orderId}`
  2. `Endpoint: {cam_ip}:8100/stopCam`
#### 2. Config folder contains crontab for camera connection, usb connection and python server.
#### 3. IMEI file contains the machine unique id.
#### 4. rc.sh is the start script which has to be included in the piś /etc/rc.local as following:
   1. `cd /home/pi/videorecorder/config`
   2. `sh rc.sh`
#### 5. Install usbmount on pi
   1. `sudo apt-get install usbmount`
#### 6. Edit usbmount conf file
   1. `sudo vim /etc/usbmount/usbmount.conf`
   2. Replace /media/usb0 to /media/pi/{MachineID} in  /etc/usbmount/usbmount.conf
   `MOUNTPOINTS="/media/usb0 /media/usb1 /media/usb2 /media/usb3
             /media/usb4 /media/usb5 /media/usb6 /media/usb7"`
             
#### 7. Install gunicorn on pi if not installed
   1. `sudo apt-get install gunicorn`
             
#### Note: 
   1. Above usbmount functionality assumes single pendrive inserted and then the order videos will be written to /media/pi/{MachineID}
   2. Make sure pendrive has single partition of FAT32 format
   
 
