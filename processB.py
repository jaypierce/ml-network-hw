######################################
#Networking with .stl files
#Developer: Jaylan Pierce
#Date: July 20, 2022
######################################

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

#Recieves stl file and tells process that it was recieved
incoming_file = None
while not incoming_file:
    incoming_file = reciever.recv_pyobj()
    sleep(1)
    reciever.send_pyobj(incoming_file)

print("File Recieved")
incoming_file.save('output_of_B.stl')
reciever.close()

#Parse File
import subprocess
subprocess.run(["python3", "parse.py", "output_of_B.stl", ">>", "output.csv"])

#Using python socket library to send stl file back
#to processA
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

host = 'localhost'
port = 5556

filename = 'output_of_B.stl'
filesize = os.path.getsize(filename)
print(filesize)

#creating client socket
s = socket.socket()
print(f"[+] Connecting to {host}:{port}")
s.connect((host,port))
print('[+] Connected')
s.send(f'{filename}{SEPARATOR}{filesize}'.encode())

#sending the file
my_mesh = stl.mesh.Mesh.from_file('output_of_B.stl')
data_string = pickle.dumps(my_mesh)
s.send(data_string)

s.close()
print("File sent")