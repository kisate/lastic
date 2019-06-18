import serial, time
import socket

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

host = '192.168.1.3'
port = 51004 # fig number

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

send(1, 2, 3)
message = read()
print(message)