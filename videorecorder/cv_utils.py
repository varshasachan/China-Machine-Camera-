import cv2
import numpy as np
import os
from datetime import datetime,timedelta

cv2_maj_ver = cv2.__version__.split('.')[0]
if cv2_maj_ver == '2':
    HISTCMPOPTION = cv2.cv.CV_COMP_BHATTACHARYYA
else:
    HISTCMPOPTION = cv2.HISTCMP_BHATTACHARYYA


class ShotChangeHist:
    def __init__(self,fps, vidLen):
        self.fps = fps
        self.vidLen = vidLen
        pass

    @staticmethod
    def getHistFeatures(frame):
        histFeats = []
        feat = ShotChangeHist.calcHistFeatOfImage(frame, bool_inputrgb=False)
        return feat

    @staticmethod
    def calcHistFeatOfImage(img, bool_inputrgb=False):
        tmp = cv2.resize(img, (120, 90))
        if bool_inputrgb:
            rgb_image = tmp
        else:
            rgb_image = cv2.cvtColor(tmp, cv2.COLOR_BGR2RGB)

        return HistCalculate.calculateHist(rgb_image)

    def getDistanceArr(self, histFeats, timestamps):
        distArr = []
        stepCount = 10
        

        for index in range(len(histFeats)):
            tempObj = {}
            tempObj[index] = []
        
            for j in range(1, stepCount):
                if index-j >= 0:
                    tempObj[index].append(HistCalculate.calculateHistDistance(histFeats[index], histFeats[index-j]))
                else:
                    break

            distArr.append(tempObj)

        print(distArr)

        return distArr

    def _getShotChange(self, arr):
        shotChange = []
        arrLen = len(arr)
        assignedArr = [0]*arrLen

        # Threshold value of min 0.25 to detect change
        for i in range(arrLen):
            if len(arr[i]) > 0:
                for (key, value) in (arr[i]).items():
                    # print(value)
                    value = np.array(value)
                    if len(value[value < 0.035]):
                        assignedArr[i] = 1

        for index in range(arrLen):
            shotChange.append(index) if assignedArr[index] == 0 else None

        shotChange = sorted(shotChange)

        return shotChange


    def obtainShotChanges(self, histFeats, timestamps):
        distArr = self.getDistanceArr(histFeats, timestamps)
        # print(len(distArr), distArr)
        totalChanges = self._getShotChange(distArr)
        print(totalChanges)

        shotChangepts = []

        for item in totalChanges:
            shotChangepts.append(timestamps[item])

        return totalChanges, shotChangepts

class HistCalculate:
    @staticmethod
    def calculateHist(rgb_image):

        # extract a 3D RGB color histogram from the image,
        # using 8 bins per channel, normalize, and update
        # the index
        hist = cv2.calcHist([rgb_image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()  # Size=8x8x8 = 512 distinct values
        return hist


    @staticmethod
    def calculateHistDistance(prevHist, nextHist):
        distance = cv2.compareHist(prevHist, nextHist, HISTCMPOPTION)
        return distance


if __name__ == '__main__':
    # print("hello
    shotChange = ShotChangeHist(30, None)

    capture = cv2.VideoCapture("people.mp4")
    print(shotChange)

    histFeats = []
    timeStamps = []

    # OUTPUT_FILE = "people.mp4"
    frame_cnt = 0
    timestamp = datetime.now()

    while(True):
        # print("here")
        ret, frame = capture.read()

        if ret:
            timestamp = timestamp + timedelta(seconds = 1)
            feat = shotChange.getHistFeatures(frame)
            # out.write(frame)
            # if utils.getChanges(frame, prev):
            #     active = active + 1
            #     change_frames.append(frame_cnt)
            if frame_cnt > 40 and frame_cnt < 100:
                cv2.imwrite("output/frame_" + str(frame_cnt) + '.jpg', frame)

            if frame_cnt > 100:
                break
            if frame_cnt % 30 == 0 and frame_cnt != 0:
                if frame_cnt/30 == 2:
                    changes, ts = shotChange.obtainShotChanges(histFeats, timeStamps)
                    changes = [x + frame_cnt - 10 for x in changes]
                    print("############",changes, frame_cnt/30)

                histFeats = histFeats[-11:-1] + [feat]
                timeStamps = timeStamps[-11:-1] + [timestamp]
            else:
                histFeats.append(feat)
                timeStamps.append(timestamp)

        else:
            break

        frame_cnt = frame_cnt + 1