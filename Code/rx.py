import encodings
import cv2
import numpy as np
import serial
import os
import base64
from time import sleep
from flask import Flask, render_template
import socket


def read():
    while(ser.in_waiting > 0):
        bytebuff += bytearray(ser.read(1))
    return bytebuff

def makeimage(byteb):
    temp = byteb.decode()
    imagedata = base64.decode(temp)
    img = cv2.imdecode(imagedata, cv2.IMREAD_COLOR)
    cv2.imwrite(savedie,img)

savedie = os.getcwd()+"/saved.jpg"
size = 1000000
bytebuff = bytearray(size)
ser = serial.Serial ("/dev/ttyS0", 19200)
while True:
    while(ser.is_open):
        if(ser.in_waiting == 1 and ser.read(1) == b'\xFE'):
            print("got the goods to read")
            print(ser.inwaiting())  
            #ser.flush()
            print("flsuhed")
            sleep(.5)
            print(ser.inwaiting)
            print("done reading")
        if(ser.in_waiting == 1 and ser.read(1) == b'\xFB'):
            print("got the good to finish read")
           # ser.flush()
            print("flush making image")
            makeimage(bytebuff)
            print("finished image")


