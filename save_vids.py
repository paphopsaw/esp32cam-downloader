import requests
import os
import numpy as np
import cv2

from datetime import datetime

r = requests.get("http://192.168.1.40", stream=True)

vidDir = "vids/"
first = False
record = False
buffer = []
imgs = []
filename = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p") + ".mp4"
size = (1200, 1600)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
framerate = 2
framePerFile = 24
numFiles = 1
vwriter = cv2.VideoWriter(os.path.join(
    vidDir, filename), fourcc, framerate, (size[1], size[0]))

num_frames = 0
fileno = 0
for b in r.iter_content():
    if (b[0] == 0xff):
        first = True
    else:
        if first & (b[0] == 0xd8):
            buffer.append(0xff)
            record = True
        elif first & (b[0] == 0xd9):
            buffer.append(b[0])
            nparray = np.asarray(buffer, np.uint8)
            img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
            vwriter.write(img)
            buffer = []
            num_frames += 1
            if (num_frames > framePerFile - 1):
                vwriter.release()
                fileno += 1
                if (fileno > numFiles - 1):
                    exit()
                filename = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p") + ".mp4"
                vwriter = cv2.VideoWriter(
                    os.path.join(vidDir, filename), fourcc, framerate, (size[1], size[0]))
                num_frames = 0

            record = False
        first = False

    if record:
        buffer.append(b[0])
