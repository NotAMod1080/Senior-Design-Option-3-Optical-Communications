import encodings
import cv2
import numpy as np
import serial
import os
import base64
from time import sleep
from picamera2 import Picamera2
from libcamera import controls
import sys

camera = Picamera2()
capture_config = camera.create_still_configuration(main={"size": (480, 480)})
camera.configure(capture_config)
ser = serial.Serial ("/dev/ttyS0", 460800)
dir = os.getcwd()+"/images/"
def nl():
    ser.write('\n'.encode('utf-8'))
#dunctions to capture and send the images
def capture():
    print("capturing")
    camera.start()
    camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    camera.capture_file(dir+"image.jpg")
    camera.stop()
def sendimage():
    filesize()
    print("sending image")
    load = cv2.imread(dir+"image.jpg")
    image = base64.b64encode(cv2.imencode('.jpg', load)[1])
    bytesize = str(len(image)).encode('utf-8')
    print(bytesize)
    ser.write(bytesize)
    nl()
    ser.write(image)
#sequence steps to tell the reciever that the image is going to be sent
def begin():
    print("sending begin")
    begin = "<<BEGIN>>".encode('utf-8')
    ser.write(begin)
    nl()
def end():
    print("sending end")
    end = "<<END>>".encode('utf-8')
    ser.write(end)
    nl()
def filesize():
    print("sending filesize")
    filesize = "<<FILE_SIZE>>".encode('utf-8')
    ser.write(filesize)
    nl()
#keeps stem active
begin()
for i in range(10):
    capture()
    sendimage()
end()
exit()