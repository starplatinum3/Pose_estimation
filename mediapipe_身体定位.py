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

def video_ope(file):
    frame = 0
    switch = True
    cap = cv2.VideoCapture(file)
    mypose= mp.solutions.pose
    pose = mypose.Pose()
    myDraw = mp.solutions.drawing_utils

    DrawingSpec_point = myDraw.DrawingSpec((0, 255, 0), 2, 2)

    while(True):
        ret, img = cap.read()
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)
        #print(results.pose_landmarks)
        if (results.pose_landmarks):
            for id,lm in enumerate(results.pose_landmarks.landmark):
                #print (id,"\n",lm)
                h,w,c  = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                print (id,cx,cy)
                if id == 0  :
                    cv2.circle(img,(cx,cy),12,(0,255,255),cv2.FILLED)
                else:
                    cv2.circle(img,(cx,cy),7,(255,0,0),cv2.FILLED)

            myDraw.draw_landmarks(img,results.pose_landmarks,mypose.POSE_CONNECTIONS,DrawingSpec_point)


        frame +=1
        cv2.putText(img,str(int(frame)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        cv2.imshow("Frame", img)
        key = cv2.waitKey(1) & 0xFF

        if key== ord('q'):
            cv2.waitKey(0)
        if key== 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    # file = "video/anime.mp4"
    file = 0
    # 摄像头
    video_ope(file)

if __name__=="__main__":
    main()
