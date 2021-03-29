from pyo import *
import time
from camera import Camera


def play(c, masterVol=100, tempo=60):
    activate = True
    attack = 1
    decay = 1
    f = Adsr(attack=attack, decay=decay, sustain=0, release=0)
    # prev = int(c.get_distance() * 3)
    # x = prev
    # w = int(c.distance_to_camera() * 4)
    # a = Sine(freq=w, mul=f).out()
    d = 0
    while activate:
        # prev = x
        f.play()
        # x = int(c.distance_to_camera(3) * 4)
        # print(x)
        a = Sine(freq=500, mul=f)
        lfo = Sine(freq=d, mul=.5, add=.5)
        d = Disto(a, drive=lfo, slope=.8, mul=.1).out()
        time.sleep(attack + decay)
        d = d + 0.1 
        print("done")
        # f.stop()
        # time.sleep(1)
        # if x >= prev:
        #     for i in range(prev, x):
        #         a = Sine(freq=i, mul=f).out()
        #         time.sleep(0.02)
        # else:
        #     for i in range(prev, x, -1):
        #         a = Sine(freq=i, mul=f).out()
        #         time.sleep(0.02)


        # a = Sine(freq=x*3, mul=f).out()
        # a = Sine(freq=x*3).out()
        # print(x)
    # f.play()
    # for i in range(10):
    #     a = Sine(freq=i*80, mul=f).out()




s = Server().boot()
s.start()
c = Camera(0)
# c.run()
# print(c.distance_to_camera(2))
play(c)

