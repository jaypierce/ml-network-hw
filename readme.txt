Synopsis:
 - Built two independent inter-communicating processes (A & B) able to exchange
   data using two different means of data transfer: ZeroMQ and Python socket library.

 - Using ZeroMQ, Process A connects with B and sends contents of the provided data 
   file cad_mesh.stl (a CAD geometry). On recieving data, B parses the data into
   a .csv file (output.csv), outputs the .stl file (output_of_B), and returns the 
   file to process A. A then saves the recieved data in a file named output_of_A.stl.

Directions:
 - Open two local machines
 - 1st machine: $python3 processA.py
 - 2nd machine: $python3 processB.py

Requirments:
 - Python 3