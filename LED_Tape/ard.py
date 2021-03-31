import pyfirmata
import time

board = pyfirmata.Arduino('/dev/cu.usbmodem141201')

it = pyfirmata.util.Iterator(board)
it.start()

blue = board.get_pin('d:5:o')
red = board.get_pin('d:6:o')
green = board.get_pin('d:7:o')

button = board.get_pin('a:0:i')
state = button.read()

while True:
    state = button.read()

    if state is not None and state > 0.0:
        blue.write(1)
    else:
        blue.write(0)