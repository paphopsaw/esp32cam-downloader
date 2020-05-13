import requests
import os

r = requests.get("http://192.168.1.40", stream=True)

frameDir = "frames/"
first = False
record = False
buffer = []
fileno = 0
filename = str(fileno) + ".jpg"
fwrite = open(os.path.join(frameDir, filename), "wb")
for b in r.iter_content():
    if (b[0] == 0xff):
        first = True
    else:
        if first & (b[0] == 0xd8):
            buffer.append(0xff)
            record = True
        elif first & (b[0] == 0xd9):
            buffer.append(b[0])
            fwrite.write(bytes(buffer))
            buffer = []
            fwrite.close()
            fileno += 1
            filename = str(fileno) + ".jpg"
            fwrite = open(os.path.join(frameDir, filename), "wb")
            record = False
        first = False

    if record:
        buffer.append(b[0])
