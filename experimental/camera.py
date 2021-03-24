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

KNOWN_DISTANCE = 18
KNOWN_WIDTH = 7.5

image = cv2.imread("images/square.jpg")
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
cap = cv2.VideoCapture(0)

prev_frames = []
while True:
    ret, frame = cap.read()
    marker = find_marker(frame)
    if marker:
        inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
        prev_frames.append(inches)
        if (len(prev_frames) == 60):
            print(median(prev_frames))
            prev_frames = []

        box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
        box = np.int0(box)
        cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
        cv2.putText(frame, "%.2fft" % (inches / 12),
            (frame.shape[1] - 200, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
            2.0, (0, 255, 0), 3)
        cv2.imshow("image", frame)
        cv2.waitKey(1)
    else:
        cv2.imshow("image", frame)
        cv2.waitKey(1)
    
cap.release()
cv2.destroyAllWindows()