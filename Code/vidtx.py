import encodings
import cv2
import numpy as np
import serial
import os
import base64
from time import sleep


ser = serial.Serial ("/dev/ttyS0", 115200)
codedprepsend = base64.b64encode(str.encode("<<READY>>"))
codedprepend = base64.b64encode(str.encode("<<EOF>>"))
vdir = os.getcwd()+"/video/kat.mp4"
idir = os.getcwd()+"/vimages/"
vidcap = cv2.VideoCapture(vdir)

def end():
   ser.write("\n".encode('utf-8'))
   sleep(.05)

def makeimages():
    def getFrame(sec):
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames,image = vidcap.read()
        if hasFrames:
            cv2.imwrite(idir+"image"+str(count)+".jpg", image)     # save frame as JPG file
        return hasFrames
    sec = 0
    frameRate = 0.5 #//it will capture image in each 0.5 second
    count=1
    success = getFrame(sec)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(sec)
    return count

print("making the images")
i = makeimages()
c = 1
print("executing send")
while (c < i):
    ser.write(codedprepsend)
    end()
    imagearray = np.array(cv2.imencode('.jpg',cv2.imread(idir+"image"+str(c)+".jpg"))[1])
    print("sending image"+str(c))
    ser.write(str(c).encode('utf-8'))
    end()
    ser.write(base64.b64encode(imagearray))
    end()
    c = c + 1
print("done")
ser.write(codedprepend)
end()
exit