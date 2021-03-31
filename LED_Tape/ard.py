import pyfirmata
import time

board = pyfirmata.Arduino('/dev/usbmodem141201')

pinMode(5, OUTPUT);
pinMode(6, OUTPUT);
pinMode(7, OUTPUT);
pinMode(A0, INPUT);
Serial.begin(9600);

it = pyfirmata.util.Iterator(board)
it.start()

blue = board.get_pin('d:5:o')
red = board.get_pin('d:6:o')
green = board.get_pin('d:7:o')

button = board.get_pin('a:0:1')

while True:
    state = button.read()

    if state == 1:
        blue.write(255)
    else:
        blue.write(0)