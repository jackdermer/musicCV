import imutils
import cv2
from statistics import median
import threading
import socket
import pickle
import time

class Camera(threading.Thread):

    def __init__(self, device_ind, callibration=1142, known_distance=36):
        super().__init__()
        self.device_ind = device_ind
        self.known_distance = known_distance
        self.known_width = 7.5
        self.current_distance = 0

        if isinstance(callibration, str):
            image = cv2.imread(callibration)
            marker = self.find_marker(image)
            self.focal_length = (marker[1][0] * self.known_distance) / self.known_width
        else:
            self.focal_length = callibration
    
    def run(self):
        cap = cv2.VideoCapture(self.device_ind)
        prev_dist = []
        while cap.isOpened():
            ret, frame = cap.read()
            marker = self.find_marker(frame)
            if marker:
                prev_dist.append(self.distance_to_camera(marker[1][0]))
                if len(prev_dist) >= 10:
                    self.current_distance = median(prev_dist)
                    prev_dist = []
        cap.release()
        cv2.destroyAllWindows()

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
            if len(approx) == 4:
                (_, _, w, h) = cv2.boundingRect(approx)
                ar = w / float(h)
                if ar >= 0.95 and ar <= 1.05:
                    return cv2.minAreaRect(approx)
    
    def distance_to_camera(self, perWidth):
	    return (self.known_width * self.focal_length) / perWidth

c0 = Camera(0)
c0.start()

c2 = Camera(2)
c2.start()

c4 = Camera(4)
c4.start()

while True:
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
