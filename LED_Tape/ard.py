import pyfirmata
import time

board = pyfirmata.Arduino('/dev/ttyACM0')

it = pyfirmata.util.Iterator(board)
it.start()

blue = board.get_pin('d:5:o')
red = board.get_pin('d:6:o')
green = board.get_pin('d:7:o')

button = board.get_pin('a:0:i')
state = button.read()

color = 1

while True:
    state = button.read()

    if state is not None and state > 0.0:
        if color % 3 == 1:
            blue.write(1)
        elif color % 3 == 2:
            red.write(1)
        else: 
            green.write(1)
    else:
        blue.write(0)
        red.write(0)
        green.write(0)
        color += 1