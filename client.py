import socket
import pickle
from pyo import *


HOST = '192.168.1.254'
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

c0 = 0
c1 = 0
c2 = 0
c3 = 0

def update_vars():
    data = s.recv(1024)
    if data:
        cams = pickle.loads(data)
        c0 = cams[0]
        c1 = cams[1]
        c2 = cams[2]
        c3 = cams[3]
        print(cams)

audio = Server().boot()
audio.start()

length = 1
scale = 3
f = Adsr(attack=length, decay=length, sustain=0, release=0)

while True:
    update_vars()
    f.play()
    a = Sine(freq=c0*scale, mul=f).out(0)
    b = Sine(freq=c1*scale, mul=f).out(0)
    c = Sine(freq=c2*scale, mul=f).out(1)
    d = Sine(freq=c3*scale, mul=f).out(1)

    time.sleep(length*2)
    
s.close()