import zmq
from time import sleep
# from stl import mesh
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

#Recieving
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((socket.gethostname(), 5556))
# s.listen(5)

# while True:
#     clientsocket, address = s.accept()
#     print(f'Connection from {address} is established')
#     clientsocket.send(bytes('Requesting stl file...', 'utf-8'))

#Better Recieving
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5556
BUFFER_SIZE = stl.stl.BUFFER_SIZE
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

recieved = client_socket.recv(BUFFER_SIZE)
# print(sys.getsizeof(recieved))

# progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open('out2.stl', "wb") as f:
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            break
        f.write(bytes_read)
client_socket.close()
s.close()

from mpl_toolkits import mplot3d
from matplotlib import pyplot

figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

my_mesh = stl.mesh.Mesh.from_file('out2.stl')
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(my_mesh.vextors))

scale = my_mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)
pyplot.show()