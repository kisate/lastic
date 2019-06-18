


import cv2 
import numpy as npy
import socket 
import time
import threading

import os, glob, pickle

import traceback
import serial, time

#TODO:
# размер экрана
# вызов нейронки
# пересчет пикселей в энкодеры


width = 1
height = 1
lastPos = 0

cameraId = 1

host = '192.168.1.3'
port = 51004 # random number

drop_off_coords = [

]


def send(*args):
    global conn

    try : 
        msg = len(args).to_bytes(1, byteorder='big')
        for a in args:
            msg += (a).to_bytes(8, byteorder='big', signed = True)
        print(msg)
        conn.send(msg)

    except BaseException as e :
        print (e)

def read():
    global conn

    message = []
    part = conn.recv(1)
    message_size = int.from_bytes(part, byteorder='big')

    for i in range(message_size):
        part = s.recv(8)
        message.append(int.from_bytes(part, byteorder='big', signed=True))

    print (message)
    if len(part) == 0 : return None
    return message

cv2.namedWindow('image')
cap = cv2.VideoCapture(cameraId)

state = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try : 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
except Exception:
    pass

s.bind(('', port))
s.listen(5)

conn, addr = s.accept()
print(addr)

arduino = serial.Serial('/dev/ttyUSB0', 115200)
time.sleep(1) 

parts = []
state = 1

while state == 1:
    try :
        message = read()

        pos = message[0]

        _, img = cap.read()
        height, width, _ = img.shape

        #data -- вывод нейронки

        
        boxes, scores, classes, num_classes = data
        
        for index in range(int(num_classes[0])):
            if (scores[0][index] > 0.9):
                box = boxes[0][index]
                classID = int(classes[0][index])
                parts.append({'id' : classID, 'center' : ((box[1] + box[3])*width/2, (box[0] + box[2])*height/2), 'enc' : pos})

        conn.send(bytes([1]))

        if (pos >= lastPos) : 
            state = 2  
    except BaseException as e:
        traceback.print_exc()
        cap.release()
        conn.close()
        exit()

num_collected = 0
num_to_collect = min(5, len(parts))
while state == 2:
    part = parts[num_collected]
    do_coords = drop_off_coords[part['id']]
    encPos = do_coords #TODO
    gripperPos = 0

    send(encPos)
    read()

    arduino.write([gripperPos >> 8])
    arduino.write([gripperPos & 256])
    arduino.read()
    
    send(do_coords[0])
    read()

    arduino.write([do_coords[1] >> 8])
    arduino.write([do_coords[1] & 256])
    arduino.read()

    num_collected += 1
    if (num_collected == num_to_collect) : state = 3
    

    
    

