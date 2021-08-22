# -*- coding: utf-8 -*-
# @Time    : 2021/8/22 9:40
# @Author  : 喵奇葩
# @FileName: mediapipe_身体定位.py.py
# @Software: IntelliJ IDEA

import cv2
import mediapipe as mp
import time
import os
import random

# https://blog.csdn.net/qq_38641985/article/details/117560289
class PoseDetector:
    def __init__(self, mode = False, upBody = False, smooth=True, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.DrawingSpec_point = self.mpDraw.DrawingSpec((0, 255, 0), 2, 2)
        # 因为没有用到 mode
        if mode:
            self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon, self.trackCon)
        else:
            self.pose = self.mpPose.Pose()
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        #print(results.pose_landmarks)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS,self.DrawingSpec_point)
        return img
    def getPosition(self, img, draw=True):
        lmList= []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    if id == 0  :
                        cv2.circle(img,(cx,cy),12,(255,255,20),cv2.FILLED)
                    else:
                        cv2.circle(img,(cx,cy),5,(255,0,0),cv2.FILLED)
            if draw:
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lmList
def main(file):
    cap = cv2.VideoCapture(file)
    frame = 0
    detector = PoseDetector()

    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.getPosition(img)
        frame+=1
        cv2.putText(img, str(int(frame)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        #cv2.waitKey(1)
        key = cv2.waitKey(1) & 0xFF

        if key== ord('q'):
            cv2.waitKey(0)
        if key== 27:
            break

    cap.release()
    cv2.destroyAllWindows()



# 可以用
if __name__=="__main__":
    # file = "video/anime.mp4"
    file = 0
    main(file)

