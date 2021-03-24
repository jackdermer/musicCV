from pyo import *
import time
s = Server().boot()
s.start()

for i in range(10):
    f = Adsr(attack=.5, decay=1, sustain=0, release=0)
    a = Sine(freq=400, mul=f).out(0)
    lf = Sine(freq=.2, mul=0.24, add=0.25)
    sd = SmoothDelay(a, delay=lf, feedback=0.5, crossfade=0.05, mul=0.7).out(1)
    f.play()
    time.sleep(2)
    f.stop()
    time.sleep(2)

# a = Sine(freq=440).out()
# f.play()
# s.gui(locals())
# d = Delay(a, delay=1, feedback=1, mul=.3).out()
# chor = Chorus(a, depth=1, feedback=0.5, bal=0.5).out()
# time.sleep(1)
# harm1 = Harmonizer(a, transpo=5, winsize=0.05).out(0)
# time.sleep(3)
# harm2 = Harmonizer(a, transpo=-2, winsize=0.05).out(1)
# time.sleep(3)
# harm2.stop()
# harm1.stop()
a.stop()
s.stop()


# time.sleep(3)
# for i in range(200,600,20):
#     a = Sine(i, 0, 0.1)
#     # d = Delay(a, delay=[.15,.2], feedback=.5, mul=.4).out()
#     time.sleep(3)
# s.stop()

# s = Server().boot()
# s.start()
# # lf = Sine([.31,.34], mul=15, add=20)
# # lf2 = LFO([.43,.41], sharp=.7, type=2, mul=.4, add=.4)
# # a = LFO(freq=lf, sharp=lf2, type=7, mul=100, add=300)
# # b = SineLoop(freq=a, feedback=0.12, mul=.2).out()
# c = LFO(type=3).out()
# time.sleep(3)
# s.stop()