import os,sys
import json
import logging
import threading
import time
import random
import serial
import cv2
import imutils
import logging

from datetime import datetime,timedelta
from flask import Flask, request
global capture, out, vs, orders_started
from imutils.video import VideoStream

app = Flask(__name__)
orders_started = 1
capture = False
vid_source = os.popen("ls /dev/video*").read().rstrip()[-1]

def get_imei():
    imei = "0000000000000000"
    try:
        with open('./config/IMEI', 'r') as imeifp:
            imei = imeifp.readline().strip()
    except Exception as e:
        print("Error fetching IMEI --> " + e.message)
        print(sys.exc_info()[0])

    return str(imei)

def dynamic_camera_info(log):
    date1 = datetime.now().strftime('%y-%m-%d')
    logfile1 = '/home/pi/videorecorder/logs/' + get_imei() + '_CAMERA_LOG_' + str(date1) + '.log'
    handler1 = logging.FileHandler(logfile1)
    logger1 = setup_logger('camera_log', handler1)
    logger1.info(log)
    logger1.removeHandler(handler1)

def setup_logger(name, handler, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger_formatter = logging.Formatter('[%(asctime)s.%(msecs)03d %(levelname)-8s] %(message)s')
    handler.setFormatter(logger_formatter)
    logger.addHandler(handler)
    return logger

@app.route("/ping")
def ping():
    return "True"


@app.route("/startCam", methods=['GET'])
def startCam():

    global capture
    print("capture"+str(capture))
    global out
    global vs
    print("Request: /startCam")
    order_id = request.args.get("order_id")
    dynamic_camera_info("Request for start order recording for " + str(order_id))

    if capture:
        dynamic_camera_info("Stopping previous order recording if it is not properly stopped")
        stopCam()
        return "False"

    thread_write = threading.Thread(target=writeVideo, args=(order_id,))
    thread_write.start()
    return "True"


def writeVideo(order_id):
    global capture
    global out
    global vs
    global orders_started
    global vid_source

    try: vs
    except NameError: vs=None

    cmd_out = os.popen("ls /dev/video*").read().rstrip()

    if len(cmd_out):
       cmd_out = cmd_out[-1]

    if vid_source != cmd_out:
       vid_source = cmd_out
       dynamic_camera_info("changed video input source:" + vid_source)
       vs = None
       dynamic_camera_info("Restarting server as the camera source is changed")
       return

    if orders_started or (vs is None):
        dynamic_camera_info("Initializing the video stream capture")
        if vid_source == '0':
           vs = VideoStream(0).start()
        elif vid_source == '1':
           vs = VideoStream(-1).start()
        else:
           dynamic_camera_info("Camera is not available")
           return "False"
        '''
        if not vs.getAvailableStatus():
            dynamic_camera_info("Camera is not available")
            return "False"
        '''
    dynamic_camera_info("Initial Camera warmup time: 2s")
    time.sleep(2.0)
    #Don't Intialize the video stream for each order, just read the frames
    orders_started = 0
    
    '''
    if not vs.getAvailableStatus():
        dynamic_camera_info("Camera is not available")
        return "False"
    '''

    capture = True
    OUTPUT_FILE = '/media/pi/' + get_imei() + '/'  + str(order_id) + '.avi'
    cv_version =  (cv2.__version__).split('.')[0]

    if cv_version == '2':
        fourcc = cv2.cv.CV_FOURCC('F', 'M', 'P', '4')
    elif cv_version == '3':
        fourcc = cv2.VideoWriter_fourcc(*'FMP4')

    out = cv2.VideoWriter(OUTPUT_FILE,fourcc, 10.0, (640,480))
    dynamic_camera_info("Writing to Output file " + OUTPUT_FILE )

    while(True):
        frame = vs.read()

        if frame is not None:
            frame = imutils.resize(frame, width=640)
            out.write(frame)

            if not capture:
                dynamic_camera_info("#######Releasing the video file#######")
                out.release()
                break


@app.route("/stopCam", methods=['GET'])
def stopCam():
    global capture
    print("Request: /stopCam")
    dynamic_camera_info("Request to close the video file")
    capture = False
    os.popen('sudo python /home/pi/videorecorder/config/checkVideoSize.py')
    return "True"
    
@app.route("/getCameraStatus", methods=['GET'])
def getCameraStatus():
    print("Request: /getCameraStatus")
    command = "curl -X GET 'https://prod-api.tinymart.in/status/capture?imei="+str(get_imei())+"&type=camera'"
    os.popen(command)
    return "True"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
