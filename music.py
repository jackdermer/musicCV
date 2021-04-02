from pyo import *
import time


def play():
    length = .8
    scale = 3
    f = Adsr(attack=length, decay=length, sustain=0, release=0)

    while True:
        #Camera 1
        # c1_dist = int(c1.current_distance)
        # print("C1_Dist: ", c1_dist)
        # print("C1_Freq: ", c1_dist * scale)
        f.play()
        a = Sine(freq=200, mul=f).out(0)
        time.sleep(length*2)

        #Camera 2
        # c2_dist = int(c2.current_distance)
        # print("C2_Dist: ", c2_dist)
        # print("C2_Freq: ", c2_dist * scale)
        f.play()
        a = Sine(freq=250, mul=f).out(0)
        time.sleep(length*2)

        #Camera 3
        # c3_dist = int(c3.current_distance)
        # print("C3_Dist: ", c3_dist)
        # print("C3_Freq: ", c3_dist * scale)
        f.play()
        a = Sine(freq=300, mul=f).out(0)
        time.sleep(length*2)

        #Camera 4
        # c4_dist = int(c4.current_distance)
        # print("C4_Dist: ", c4_dist)
        # print("C4_Freq: ", c4_dist * scale)
        f.play()
        a = Sine(freq=350, mul=f).out(0)
        time.sleep(length*2)


s = Server().boot()
s.start()
# c1 = Camera(0)
# c2 = Camera(1)
# c3 = Camera(3)
# c4 = Camera(4)
# c1.start()
# c2.start()
# c3.start()
# c4.start()

play()



        # lfo = Sine(freq=d, mul=.5, add=.5)
        # d = Disto(a, drive=lfo, slope=.8, mul=.1).out()
        # d = d + 0.1 
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