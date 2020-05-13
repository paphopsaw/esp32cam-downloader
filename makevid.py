import numpy as np
import cv2
import os


frameDir = "frames/"
video_name = "vid.mp4"
numFrames = 47
size = (1200, 1600)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
framerate = 4.8
video = cv2.VideoWriter(video_name, fourcc, framerate, (size[1], size[0]))

img_array = []
for i in range(numFrames):
    filename = str(i) + ".jpg"
    fd = open(os.path.join(frameDir, filename), "rb")
    img_str = fd.read()
    fd.close()
    nparray = np.asarray(bytearray(img_str), np.uint8)
    img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
    video.write(img)

video.release()
