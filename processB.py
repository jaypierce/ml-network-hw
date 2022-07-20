from time import sleep
import zmq
import socket as netsocket
from stl import mesh

#Setting up ZeroMQ subscriber
context = zmq.Context()
sender = context.socket(zmq.REP)
sender.bind('tcp://127.0.0.1:5555')

#Recieves stl file and sends it back to process A
incoming_file = None
while not incoming_file:
    incoming_file = sender.recv_pyobj()

    sleep(1)

    sender.send_pyobj(incoming_file)


print("File Recieved")
incoming_file.save('out.stl')

#TODO: Parse File

#Sending the file back
# s = netsocket.socket()
# host = netsocket.gethostname()
# port = 5555
# s.bind((host,port))
# print(host)
# s.listen(1)

# print("Waiting for incoming connections...")
# conn, addr = s.accept()
# print("Connected")