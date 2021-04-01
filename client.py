import socket
import pickle

HOST = '192.168.1.254'
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    data = s.recv(1024)
    print(pickle.loads(data))
    
s.close()