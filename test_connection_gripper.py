from ev3socketclient import Client
import time
host = '192.168.1.3'
port = 51004 # fig number


class MessageHandler():
    def __init__(self):
        self.state = 0
        self.message = []
    
    def updateMessage(self, message):
        self.message = message
        self.state = message[0]
        print("in handler : " + str(message) + " " + str(self.state))


def waitForCommand():

    while True:
        try :
            if (messagehandler.state == 0):
                time.sleep(0.005)

            if (messagehandler.state == 1):
                message = messagehandler.message
                print(message)
                messagehandler.state = 0
                client.send(100, 233, 123)

                
                
        except BaseException as e:
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print (e)
            break

client = Client(host, port)
messagehandler = MessageHandler()
client.connect(messagehandler)
