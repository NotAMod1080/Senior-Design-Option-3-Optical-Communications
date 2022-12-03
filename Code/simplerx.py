import encodings
import cv2
import numpy as np
import serial
import os
import base64
from time import sleep
from flask import Flask, render_template
import socket

ser = serial.Serial ("/dev/ttyS0", 9600)
while True:
    while(ser.is_open):
        if(ser.inwaiting > 0):
            print(ser.read(1))