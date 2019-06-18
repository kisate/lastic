#!/usr/bin/env python3
import smbus, threading
from threading import Thread

import time

from math import acos, pi

from ev3dev2.motor import LargeMotor, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_A, OUTPUT_C, MediumMotor, OUTPUT_D
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import TouchSensor

from ev3socketclient import Client

servoAddresses = [0x42, 0x43, 0x44, 0x45, 0x46, 0x47]


droneLeft = False

lastMessage = []

host = '192.168.1.3'
port = 51004 # fig number

moving_motor = LargeMotor(OUTPUT_A)

client = Client(host, port)


def rideToEnc(enc, percent = 100):
    position = moving_motor.position

    print ("Riding to {}".format(enc))

    if position < enc:
        moving_motor.on(SpeedPercent(percent))
        while moving_motor.position < enc:
            time.sleep(0.001)
            client.send(1, moving_motor.position)
        moving_motor.stop()
    elif position > enc:
        moving_motor.on(SpeedPercent(-percent))
        while moving_motor.position > enc:
            time.sleep(0.001)
            client.send(1, moving_motor.position)
        moving_motor.stop()
                    

def finish():
    moving_motor.reset()
    
    client.disconnect()


class MessageHandler():
    def __init__(self):
        self.state = 0
        self.message = []
    
    def updateMessage(self, message):
        self.message = message
        self.state = message[0]
        print("in handler : " + str(message) + " " + str(self.state))

messagehandler = MessageHandler()

def waitForCommand():

    while True:
        try :
            if (messagehandler.state == 0):
                time.sleep(0.005)

            if (messagehandler.state == 1):
                message = messagehandler.message
                print(message)
                messagehandler.state = 0

                rideToEnc(moving_motor.position + 500)

                client.socket.send(moving_motor.position.to_bytes(2, 'big'))
            
            if (messagehandler.state == 2):
                message = messagehandler.message
                print(message)

                pos = message[1]
                rideToEnc(pos)
                client.send(1)
                
                
        except BaseException as e:
            finish()
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print (e)
            break

time.sleep(5)
moving_motor.stop()

print("connecting")
client.connect(messagehandler)
print("connected")

time.sleep(0.2)

waitForCommand()

finish()