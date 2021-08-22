import cv2
import mediapipe as mp
import time

# Python 3.7.7 (tags/v3.7.7:d7c567b08f, Mar 10 2020, 10:41:24) [MSC v.1900 64 bit (AMD64)] on win32
# mediapipe                                 0.8.7
# 注意版本问题 特别是 mediapipe ，好像py3.7.4 是装不了的，只有 Python 3.7.7  可以装。而且 mediapipe 0.8.7 貌似废弃了
# FACE_CONNECTIONS  使用了 更牛逼的 FACEMESH_TESSELATION（应该是网格的吧，反正感觉更密了）
# 这个根据 github 版本对比可以看到
# 比如
# https://github.com/google/mediapipe/compare/v0.8.4...v0.8.7
class PoseDetector:

    def __init__(self, mode = False, upBody = False, smooth=True, detectionCon = 0.5, trackCon = 0.5,model_complexity=1):

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        # https://google.github.io/mediapipe/solutions/pose#static_image_mode.
        # 不知道 upBody 是什么 总之根据他的构造函数，这个参数应该是被废弃了
        try:
            self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon, self.trackCon)
        except TypeError as e:
            # print(e.__class__)
            # <class 'TypeError'>
            self.pose = self.mpPose.Pose(static_image_mode=self.mode,
                                         model_complexity=model_complexity,
                                         smooth_landmarks=self.smooth,
                                         min_detection_confidence=self.detectionCon,
                                         min_tracking_confidence=self.trackCon)
        # static_image_mode=False,
        # model_complexity=1,
        # smooth_landmarks=True,
        # enable_segmentation=False,
        # smooth_segmentation=True,
        # min_detection_confidence=0.5,
        # min_tracking_confidence=0.5):

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        #print(results.pose_landmarks)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img

    def getPosition(self, img, draw=True):
        lmList= []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                #print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lmList

# https://blog.csdn.net/woshicver/article/details/117004577
def main():
    cap = cv2.VideoCapture('videos/a.mp4')
    pTime = 0
    detector = PoseDetector()
    # 用了这个就有问题 可能是版本问题？
    while True:
        success, img = cap.read()
        if not success:
            print("视频结束")
            break
        img = detector.findPose(img)
        lmList = detector.getPosition(img)
        print(lmList)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()