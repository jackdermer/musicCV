import socket
import pickle
from pyo import *


HOST = '192.168.1.254'
PORT = 8887

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
        global c0
        global c1
        global c2
        global c3
        c0 = cams[0]
        c1 = cams[1]
        c2 = cams[2]
        c3 = cams[3]
        print(cams)

audio = Server().boot()
audio.start()

length = 0.5
scale = 3
f = Adsr(attack=length, decay=length, sustain=0, release=0)

while True:
    update_vars()
    f.play()
    a = Sine(freq=c0, mul=f).out(0)
    time.sleep(length*2)
    f.play()
    b = Sine(freq=c1, mul=f).out(0)
    time.sleep(length*2)
    f.play()
    c = Sine(freq=c2, mul=f).out(0)
    time.sleep(length*2)
    f.play()
    d = Sine(freq=c3, mul=f).out(0)
    time.sleep(length*2)
    
s.close()