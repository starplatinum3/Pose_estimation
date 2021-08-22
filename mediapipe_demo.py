import sys
from cv2 import cv2
import mediapipe as mp
import math

def getAngle( firstPoint,  midPoint,  lastPoint):
  front=math.atan2(lastPoint.getPosition().y - midPoint.getPosition().y,lastPoint.getPosition().x - midPoint.getPosition().x)
  back=math.atan2(firstPoint.getPosition().y - midPoint.getPosition().y,firstPoint.getPosition().x - midPoint.getPosition().x)
  result =math.degrees(front-back)
  result = math.abs(result) # Angle should never be negative
  if (result > 180):
    result = (360.0 - result)
    # Always get the acute representation of the angle
  
  return result

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
# For webcam input:
cap = cv2.VideoCapture(0)

def getAngleOfLandmarks(landmarks):
  for i in landmarks:
    print(i)
  # if len(landmarks)>3:
  #   angle=getAngle(landmarks[0],landmarks[1],landmarks[2])
  #   print("angle",angle)
# https://blog.csdn.net/menglir/article/details/116137112


def Normalize_landmarks(image, hand_landmarks):
  new_landmarks = []
  for i in range(0,len(hand_landmarks.landmark)):
    float_x = hand_landmarks.landmark[i].x
    float_y = hand_landmarks.landmark[i].y
    # Z坐标靠近屏幕增大，远离屏幕减小
    float_z = hand_landmarks.landmark[i].z
    # print(float_z)
    width = image.shape[1]
    height = image.shape[0]
 
    pt = mp_drawing._normalized_to_pixel_coordinates(float_x,float_y,width,height)
    new_landmarks.append(pt)
  return new_landmarks


# 好稳定
# 也没有装什么特别的东西 怎么就可以用啊 ，那个代码就不行
with mp_hands.Hands(
    min_detection_confidence=0.9,
    min_tracking_confidence=0.9) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue
 
    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    # 水平翻转图像，以便稍后显示自拍视图，然后转换
#将BGR图像转换为RGB。
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)
 
    # Draw the hand annotations on the image.
    # 在图像上绘制手部注释。
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image_hight, image_width, _ = image.shape
    # 陆标，地标 multi_hand_landmarks
    marks=results.multi_hand_landmarks
    if results.multi_hand_landmarks:
      # print("results.multi_hand_landmarks",results.multi_hand_landmarks)
      # print(len(marks))
      # 长度 1
      # if len(marks)>3:
      #   angle=getAngle(marks[0],marks[1],marks[2])
      #   print("angle",angle)
      # hand_landmarks_lst=[]
      print("=================")
      for hand_landmarks in results.multi_hand_landmarks:
        # print("hand_landmarks:",hand_landmarks)
        # hand_landmarks_lst.append(hand_landmarks)
        # print(hand_landmarks)
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        # getAngleOfLandmarks(hand_landmarks)
        # 这是哪几个点
        new_landmarks=Normalize_landmarks(image,hand_landmarks)
        print(new_landmarks)
        # print("mp_hands.HandLandmark.INDEX_FINGER_TIP",mp_hands.HandLandmark.INDEX_FINGER_TIP)
#         =================
# mp_hands.HandLandmark.INDEX_FINGER_TIP HandLandmark.INDEX_FINGER_TIP
# Index finger tip coordinates: ( 180.18707275390625, 374.5967102050781)
        # 这就是个字符串
        print(
        f'Index finger tip coordinates: (',
        f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
        f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_hight})'
      )
      # if len(hand_landmarks_lst)>3:
      #   angle=getAngle(hand_landmarks_lst[0],hand_landmarks_lst[1],hand_landmarks_lst[2])
      #   print("angle",angle)
    cv2.imshow('MediaPipe Hands', image)
    # 等待的  esc
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()