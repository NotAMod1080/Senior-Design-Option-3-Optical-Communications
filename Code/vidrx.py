import sys
import encodings
import cv2
import numpy as np
import serial
import os
import base64
from time import sleep
from flask import Flask, render_template
import socket
import threading

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('web.html')

#creates tgread for web page and the time sensitive stuff will be on main thread
if __name__ == '__main__':
    t1 = threading.Thread(target=lambda: app.run(debug=False,host=get_ip())).start()

#statics for recived status
begin = b'<<BEGIN>>\n'
end = b'<<END>>\n'
filesize = b'<<FILE_SIZE>>\n'

ser = serial.Serial ("/dev/ttyS0", 460800)
dir = os.getcwd()+"/images/"
webdir = os.getcwd()+"/static/images/"
print("welcome to the program")
#recived inofromation in a sequential order ADD WATCHDOG TO RESET IN CASE OF MISSED PACKET
def recieve(i):
    print("before waiting")
    readin = ser.readline()
    if(readin == begin):
        print("waiting for images")
    if(readin == end):
        print("End has been declared goodbye")
        t1.join()
        exit()
    if(readin == filesize):
        print("getting image")
        i = getimage(int(ser.readline().decode('utf-8')), i)
        print("image saved")
    return i
def getimage(bytesize, i):
    rawimage = ser.read(bytesize)
    processedimage = base64.b64decode(rawimage)
    with open(dir+str(i)+"image.jpg",'wb') as file:
        file.write(processedimage)
    file.close()
    with open(webdir+"image.jpg",'wb') as file:
        file.write(processedimage)
    file.close()
    #app.render_template('web.html')
    i = i + 1
    return i
#keeps the recieved alive
i = 0
while True:
    i = recieve(i)