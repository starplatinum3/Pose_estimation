import cv2
import mediapipe as mp
from os import listdir
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
 
 
# For static images:
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=5,
    min_detection_confidence=0.2)
img_path = './multi_hands/'
save_path = './'
index = 0
file_list = listdir(img_path) 
for filename in file_list:
  index += 1
  file_path = img_path + filename
  # Read an image, flip it around y-axis for correct handedness output (see
  # above).
  image = cv2.flip(cv2.imread(file_path), 1)
  # Convert the BGR image to RGB before processing.
  results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
 
 
  # Print handedness and draw hand landmarks on the image.
  print('Handedness:', results.multi_handedness)
  if not results.multi_hand_landmarks:
    continue
  image_hight, image_width, _ = image.shape
  annotated_image = image.copy()
  for hand_landmarks in results.multi_hand_landmarks:
    print('hand_landmarks:', hand_landmarks)
    print(
        f'Index finger tip coordinates: (',
        f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
        f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_hight})'
    )
    mp_drawing.draw_landmarks(
        annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
  cv2.imwrite(
      save_path + str(index) + '.png', cv2.flip(annotated_image, 1))
hands.close()
 
 
# For webcam input:
hands = mp_hands.Hands(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)
while cap.isOpened():
  success, image = cap.read()
  if not success:
    print("Ignoring empty camera frame.")
    # If loading a video, use 'break' instead of 'continue'.
    continue
 
 
  # Flip the image horizontally for a later selfie-view display, and convert
  # the BGR image to RGB.
  image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
  # To improve performance, optionally mark the image as not writeable to
  # pass by reference.
  image.flags.writeable = False
  results = hands.process(image)
 
 
  # Draw the hand annotations on the image.
  image.flags.writeable = True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
      mp_drawing.draw_landmarks(
          image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
  cv2.imshow('result', image)
  if cv2.waitKey(5) & 0xFF == 27:
    break
cv2.destroyAllWindows()
hands.close()
cap.release()