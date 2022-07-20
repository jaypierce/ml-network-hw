from importlib.resources import open_binary
from time import sleep
import zmq
import socket
import os
import pickle
import stl

#Setting up ZeroMQ subscriber
context = zmq.Context()
reciever = context.socket(zmq.REP)
reciever.bind('tcp://127.0.0.1:5555')

#Recieves stl file and sends it back to process A
incoming_file = None
while not incoming_file:
    incoming_file = reciever.recv_pyobj()

    sleep(1)

    reciever.send_pyobj(incoming_file)


print("File Recieved")
incoming_file.save('out.stl')
reciever.close()

#TODO: Parse File

#Sending the file back
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((socket.gethostname(), 5556))

# while True:
#     msg = s.recv(1024)
#     print(msg.decode("utf-8"))


#Better Sending
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

host = 'localhost'
port = 5556

filename = 'out.stl'
filesize = os.path.getsize(filename)
print(filesize)

#creating client socket
s = socket.socket()
print(f"[+] Connecting to {host}:{port}")
s.connect((host,port))
print('[+] Connected')
s.send(f'{filename}{SEPARATOR}{filesize}'.encode())
# print(type(filename))
my_mesh = stl.mesh.Mesh.from_file('out.stl')

# print(my_mesh)
data_string = pickle.dumps(my_mesh)
s.send(data_string)

#sending the file
s.close()
print("File sent")