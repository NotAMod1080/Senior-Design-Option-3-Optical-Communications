import encodings
import cv2
import numpy as np
import serial
import os
import base64
from time import sleep


ser = serial.Serial ("/dev/ttyS0", 19200)   #Open port with baud rate
data = "Wassup"
sdata = str.encode(data)
dir = os.getcwd()+"/image.jpg"
savedie = os.getcwd()+"/saved.jpg"
ima = cv2.imread(dir)
imbytedata = np.array(cv2.imencode('.jpg', ima)[1])
sendabledata = base64.b64encode(imbytedata)
img = cv2.imdecode(imbytedata, cv2.IMREAD_COLOR)
cv2.imwrite(savedie,img)
print("sedning data")
send = b'\xFE'
ser.write(send)
sleep(.5)
ser.write(sendabledata)
sleep(.5)
res =b'\xFB'
ser.write(res)
print("done")
#while True:
   # ser.write(sdata)
   # sleep(1)