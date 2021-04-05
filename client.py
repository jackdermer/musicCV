import socket
import pickle
from pyo import *
import sys
import threading


HOST = '172.18.131.47'
PORT = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

c0 = 0
c1 = 0
c2 = 0
c3 = 0

class Update_Vars(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.data = pickle.loads(s.recv(1024))
    
    def run(self):
        while True:
            self.data = pickle.loads(s.recv(1024))

audio = Server().boot()
audio.start()

cam_vars = Update_Vars()
cam_vars.start()

length = .5
scale = 6
f = Adsr(attack=length, decay=length, sustain=0, release=0)

while True:
    c_list = cam_vars.data
    print(c_list)
    c0 = c_list[0]
    c1 = c_list[1]
    c2 = c_list[2]
    c3 = c_list[3]
    
    f.play()
    a = Sine(freq=c0*scale, mul=f).out(0)
    time.sleep(length*2)
    
    c_list = cam_vars.data
    c0 = c_list[0]
    c1 = c_list[1]
    c2 = c_list[2]
    c3 = c_list[3]

    f.play()
    a = Sine(freq=c1*scale, mul=f).out(0)
    time.sleep(length*2)

    c_list = cam_vars.data
    c0 = c_list[0]
    c1 = c_list[1]
    c2 = c_list[2]
    c3 = c_list[3]

    f.play()
    a = Sine(freq=c2*scale, mul=f).out(0)
    time.sleep(length*2)

    c_list = cam_vars.data
    c0 = c_list[0]
    c1 = c_list[1]
    c2 = c_list[2]
    c3 = c_list[3]


    f.play()
    a = Sine(freq=c3*scale, mul=f).out(0)
    time.sleep(length*2)
    
s.close()