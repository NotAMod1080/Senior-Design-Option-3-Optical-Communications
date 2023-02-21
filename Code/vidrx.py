import encodings
import cv2
import numpy as np
import serial
import os
import base64
from time import sleep

ser = serial.Serial ("/dev/ttyS0", 115200)
savedie = os.getcwd()+"/images/"
line = ""
ready = b'<<READY>>'
end = b'<<EOF>>'
#Make this spawn a thread that will kill itself to speed up the process, maybe dump the file readline could be quicker 
def readinamge(imagename):
    with open(savedie+"image"+imagename+".jpg",'wb') as file:
        file.write(base64.b64decode(ser.readline()))

print("waiting")
while True:
    dline = ser.readline()
    line = base64.b64decode(dline)
    if line == ready:
        print("ready recieved")
        line = ""
        name = ser.readline()
        print("the name recieved is"+str(name)+" or "+name.decode('utf-8'))
        readinamge(name.decode('utf-8'))
    if line == end:
        print("the end has been reached")
        line = ""
        exit
