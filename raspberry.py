import cv2
from statistics import median
import socket
import pickle
import time
import pyfirmata
import signal
import sys

def callibrate(img_path, known_width, known_distance):
    img = cv2.imread(img_path)
    face = find_face(img)
    return face[2] * known_distance / known_width

def find_face(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 8)
    if len(faces) > 0:
        return sorted(faces, key=lambda x: x[2], reverse=True)[0]

class Camera:
    def __init__(self, device_ind, always_on=False, known_width=5.5, known_distance=26, cal_img='images/face.jpg'):
        self.known_width = known_width
        self.focal_length = callibrate(cal_img, known_width, known_distance)
        
        self.current_distance = 0
        
        self.device_ind = device_ind
        self.always_on = always_on
        if self.always_on:
            self.cap = cv2.VideoCapture(self.device_ind)            
    
    def distance_to_camera(self, per_width):
        return (self.known_width * self.focal_length) / per_width

    def update_distance(self):
        if self.always_on:
            cap = self.cap
        else:
            cap = cv2.VideoCapture(self.device_ind)
        if cap.isOpened():
            dists = []
            for i in range(1):
                _, frame = cap.read()
                if frame is not None:
                    face = find_face(frame)
                    if face is not None:
                        # print(f"{self.device_ind} found face!")
                        # dists.append(self.distance_to_camera(face[2]))
                        self.current_distance = self.distance_to_camera(face[2])
                else:
                    print(f"Frame Error: {self.device_ind}")
            if len(dists) > 0:
                self.current_distance = median(dists)
        else:
            print(f"Cap Error: {self.device_ind}")
        if not self.always_on:
            cap.release()

def signal_handler(sig, frame):
    global conn
    global sock
    print("Exiting gracefully")
    if conn:
        print("Closing conn")
        conn.close()
    if sock:
        print("Closing sock")
        sock.close()
    exit(0)

if len(sys.argv) != 2:
    print("Usage: raspberry.py <port>")
    exit()

signal.signal(signal.SIGINT, signal_handler)

board = pyfirmata.Arduino('/dev/ttyACM0')

it = pyfirmata.util.Iterator(board)
it.start()

blue = board.get_pin('d:7:o')
red = board.get_pin('d:6:o')
green = board.get_pin('d:5:o')

button = board.get_pin('a:0:i')
state = button.read()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("172.18.131.47", int(sys.argv[1])))
sock.listen(1)

while True:
    state = button.read()
    blue.write(1)
    if state is not None and state > 0.0:
        blue.write(0)
        red.write(1)
        print("seting up cameras...")
        
        c0 = Camera(0)
        c2 = Camera(2)
        c4 = Camera(4)
        c6 = Camera(6)

        time.sleep(1)
        print("cameras set up")

        red.write(0)
        time.sleep(0.3)
        red.write(1)
        print("waiting for connection")
        conn, addr = sock.accept()
        print("connection established")

        red.write(0)
        green.write(1)
        print("running program")

        state = button.read()
        while state is None or state <=0.0:
            c0.update_distance()
            c2.update_distance()
            c4.update_distance()
            c6.update_distance()

            c0_dist = int(c0.current_distance)
            print("C0_Dist: ", c0_dist)
            print()

            c2_dist = int(c2.current_distance)
            print("C2_Dist: ", c2_dist)
            print()

            c4_dist = int(c4.current_distance)
            print("C4_Dist: ", c4_dist)
            print()

            c6_dist = int(c6.current_distance)
            print("C6_Dist: ", c6_dist)
            print()

            conn.send(pickle.dumps([c0_dist, c2_dist, c4_dist, c6_dist]))
        
            state = button.read()
        
        print("Ending program")
        
        conn.close()


        green.write(0)
        red.write(1)
        time.sleep(2)
        print("Ready to Run")
        red.write(0)
