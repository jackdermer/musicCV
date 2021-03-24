from imutils import paths
import numpy as np
import imutils
import cv2
from statistics import median

def find_marker(image):
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
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            if ar >= 0.95 and ar <= 1.05:
                return cv2.minAreaRect(approx)

def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth

class Camera:
    def __init__(self):
        self.KNOWN_DISTANCE = 18
        self.KNOWN_WIDTH = 7.5

        image = cv2.imread("images/square.jpg")
        marker = find_marker(image)
        self.focalLength = (marker[1][0] * self.KNOWN_DISTANCE) / self.KNOWN_WIDTH
    
    def get_distance(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            marker = find_marker(frame)
            if marker:
                return distance_to_camera(self.KNOWN_WIDTH, self.focalLength, marker[1][0])
        cap.release()
        cv2.destroyAllWindows()

c = Camera()