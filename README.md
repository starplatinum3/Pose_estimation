# Pose_estimation

### 2021年8月22日10:40:03

代码都是网上复制的，我就是修改了些版本bug，还有自己的拙劣注释。。
代码的真正作者可以直接复制一段代码上百度搜，一般都能搜到原文了
有几个代码我也把原文链接贴上了

###  版本问题

 Python 3.7.7 (tags/v3.7.7:d7c567b08f, Mar 10 2020, 10:41:24) [MSC v.1900 64 bit (AMD64)] on win32

 mediapipe                                 0.8.7
 
 注意版本问题 特别是 mediapipe ，好像py3.7.4 是装不了的，只有 Python 3.7.7  可以装。而且 mediapipe 0.8.7 貌似废弃了
 FACE_CONNECTIONS  使用了 更牛逼的 FACEMESH_TESSELATION（应该是网格的吧，反正感觉更密了）
 
 这个根据 github 版本对比可以看到
 
 比如
 https://github.com/google/mediapipe/compare/v0.8.4...v0.8.7

如果运行有问题 有可能是各种包的版本问题，可以看python moudle version.log


## 草稿

pip3.7 install mediapipe

pip install mediapipe

```
G:\environment\python37\Scripts>pip install mediapipe
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
ERROR: Could not find a version that satisfies the requirement mediapipe (from versions: none)
ERROR: No matching distribution found for mediapipe
```



###  原来的文档
Pose estimation</br>

libraries:</br>
--> pip install opencv-python</br>
--> pip install mediapipe</br>


