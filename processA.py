import zmq
from time import sleep
from stl import mesh
import socket as netsocket

#Sending
#Setting up ZeroMQ publisher
context = zmq.Context()
# sender = context.socket(zmq.PUB)
# sender.bind('tcp://127.0.0.1:5555')

file = mesh.Mesh.from_file('cad_mesh.stl')
print("Sending stl file...")

sender = context.socket(zmq.REQ)
sender.connect('tcp://127.0.0.1:5555')
#################################################

#Recieving
# s = netsocket.socket()
# host = input(str("Enter host address:"))
# port = 5555
# s.connect((host, port))

# print("Connected!")

# print("Waiting to recieve file...")
################
arrived = None
while not arrived:
    sender.send_pyobj(file)
    arrived = sender.recv_pyobj()

print(type(arrived))
#############
# recieved = None
# while(not recieved):
#     sender.send_pyobj(file)
#     try:
#         reciever.send_string("Confirmed")
#     except:
#         sleep(1) 
#         try:
#             print("got it")
#             recieved = reciever.rcvmore()
#             print('MMMMMM')
#         except:
#             print("No confirmation of receipt")

# while True:
#     if recieved:
#         break
#     sender.send_pyobj(file)
#     try:
#         reciever.send_string('')
#     except:
#         try:
#             recieved = reciever.recv()
#         except:
#             print("No reply")


print("Recieved confimation!")


