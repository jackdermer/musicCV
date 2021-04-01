import imutils
import cv2
from statistics import median
import socket
import pickle
import time
import pyfirmata

class Camera:
    def __init__(self, device_ind, callibration=1142, known_distance=36):
        self.device_ind = device_ind
        self.current_distance = 0

        self.known_distance = known_distance
        self.known_width = 7.5

        if isinstance(callibration, str):
            image = cv2.imread(callibration)
            marker = self.find_marker(image)
            self.focal_length = (marker[1][0] * self.known_distance) / self.known_width
        else:
            self.focal_length = callibration

    
    def find_marker(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 35, 125)

        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            return cv2.minAreaRect(approx)
            # if len(approx) == 4:
                # (_, _, w, h) = cv2.boundingRect(approx)
                # ar = w / float(h)
                # if ar >= 0.95 and ar <= 1.05:
                #     return cv2.minAreaRect(approx)
    
    def update_distance(self):
        cap = cv2.VideoCapture(self.device_ind)
        if cap.isOpened():
            ret, frame = self.cap.read()
            if frame is not None:
                marker = self.find_marker(frame)
                if marker:
                    self.current_distance = self.distance_to_camera(marker[1][0])
            else:
                print(f"Error frame none {self.device_ind}")
        else:
            print(f"Error cap not open {self.device_ind}")
        cap.release()

        # if not self.cap.isOpened():
        #     print(f"Error camera {self.device_ind} failed")
        #     self.kill()
        #     self.cap = cv2.VideoCapture(self.device_ind)
        # if self.cap.isOpened():
        #     ret, frame = self.cap.read()
        #     if frame is None:
        #         print(f"Error camera {self.device_ind} failed")
        #         self.kill()
        #         self.cap = cv2.VideoCapture(self.device_ind)
        #     else:
        #         marker = self.find_marker(frame)
        #         if marker:
        #             self.current_distance = self.distance_to_camera(marker[1][0])
    
    # def kill(self):
    #     self.cap.release()
    
    def distance_to_camera(self, perWidth):
	    return (self.known_width * self.focal_length) / perWidth

board = pyfirmata.Arduino('/dev/ttyACM0')

it = pyfirmata.util.Iterator(board)
it.start()

blue = board.get_pin('d:7:o')
red = board.get_pin('d:6:o')
green = board.get_pin('d:5:o')

button = board.get_pin('a:0:i')
state = button.read()



while True:
    state = button.read()
    blue.write(1)
    if state is not None and state > 0.0:
        blue.write(0)
        red.write(1)
        print("starting cameras...")
        
        c0 = Camera(0)
        c2 = Camera(2)
        c4 = Camera(4)

        time.sleep(3)
        state = button.read()
        print("cameras running")
        red.write(0)
        green.write(1)

        while state is None or state <=0.0:
            c0.update_distance()
            c2.update_distance()
            c4.update_distance()

            c0_dist = int(c0.current_distance)
            print("C0_Dist: ", c0_dist)
            print()

            c2_dist = int(c2.current_distance)
            print("C2_Dist: ", c2_dist)
            print()

            c4_dist = int(c4.current_distance)
            print("C4_Dist: ", c4_dist)
            print()

            time.sleep(1)
        
            state = button.read()
        
        print("Ending program")
        
        c0.kill()
        c2.kill()
        c4.kill()
        
        green.write(0)
        red.write(1)
        time.sleep(2)
        print("Ready to Run")
        red.write(0)

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind(("localhost", 8888))
# sock.listen(1)
# while True:
#     conn, addr = sock.accept()
#     c = 0
#     while True:
#         conn.send(pickle.dumps([c, c, c, c]))
#         c += 1
#         time.sleep(1)
# conn.close()
