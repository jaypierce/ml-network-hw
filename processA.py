import zmq
from time import sleep
import pickle
import stl
import socket
import tqdm
import os
import sys

#Sending
#Setting up ZeroMQ publisher
context = zmq.Context()
# sender = context.socket(zmq.PUB)
# sender.bind('tcp://127.0.0.1:5555')

file = stl.mesh.Mesh.from_file('cad_mesh.stl')
print("Sending stl file...")

sender = context.socket(zmq.REQ)
sender.connect('tcp://127.0.0.1:5555')
#################################################

#Sending file to process b and waiting for a
#response before moving on
arrived = None
while not arrived:
    sender.send_pyobj(file)
    arrived = sender.recv_pyobj()

print("Recieved confimation!")
sender.close()

#Better Recieving
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5556
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

#Creating socket
s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
client_socket, address = s.accept()
print(f"[+] {address} is connected.")

received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename)
print(filesize)
# filesize = int(filesize)

# recieved = client_socket.recv(10000)
# print(sys.getsizeof(recieved))

incoming = b""
while True:
    packet = client_socket.recv(4096)
    if not packet: break
    incoming += packet

incoming_arr = pickle.loads(incoming)
print(incoming_arr)
incoming_arr.save('out2.stl')


# with open('out2.stl', "wb") as f:
#     i = 0
#     while i <= int(filesize):
#         bytes_read = client_socket.recv(BUFFER_SIZE)
#         if not bytes_read:    
#             break
#         f.write(bytes_read)
#         i += BUFFER_SIZE
    
client_socket.close()
s.close()

