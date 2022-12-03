import serial
import os
import base64
from time import sleep


ser = serial.Serial ("/dev/ttyS0", 9600)   #Open port with baud rate
data = "A"
sdata = str.encode(data)

while True:
    ser.write(sdata)