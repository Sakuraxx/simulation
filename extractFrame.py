import cv2
import time
from constant import *

def extract_one_frame():
    # 读取视频文件
    videoCapture = cv2.VideoCapture(VIDEO_FILE)

    # 读帧
    success, frame = videoCapture.read()
    i = 0
    # 设置固定帧率
    timeF = 30
    j = 0
    threshold = 2
    t1 = time.perf_counter()
    while success:
        i = i + 1
        if i >= threshold: break
        success, frame = videoCapture.read()
    # cv2.imwrite('./data/image.jpg', frame) # 只抽取2ms 加上写文件32ms
    t2 = time.perf_counter()
    # print((t2 - t1) * 1000)
