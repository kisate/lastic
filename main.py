


import cv2 
import numpy as npy
import socket 
import time
import threading

import os, glob, pickle

import traceback
from getkey import getkey, keys
from time import sleep

#TODO:
# размер экрана
# вызов нейронки
# пересчет пикселей в энкодеры


width = 1
height = 1
lastPos = 0

cameraId = 1

host = '192.168.1.3'
port = 51100 # random number
a = False

q = []

changed_id = []
changed_stats = []
CLIENT_ID = "733b83d64f87370"

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

state = 1

while state == 1:
    try :
        pos = conn.recv(2)
        pos = int.from_bytes(pos, 'big')
        _, img = cap.read()
        height, width, _ = img.shape

        #data -- вывод нейронки

        parts = []
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