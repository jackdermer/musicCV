# import the necessary packages
from imutils import paths
import numpy as np
import imutils
import cv2

def find_marker(image):
    # convert the image to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)
    # find the contours in the edged image and keep the largest one;
    # we'll assume that this is our piece of paper in the image
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts) 
    # c = max(cnts, key = cv2.contourArea)
	# compute the bounding box of the of the paper region and return it
    # return cv2.minAreaRect(c)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.1 * peri, True)
        if len(approx) == 4:
            # return cv2.minAreaRect(approx)
            (_, _, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            if ar >= 0.95 and ar <= 1.05:
                return cv2.minAreaRect(approx)

def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth

# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 36.0
# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide
KNOWN_WIDTH = 7.5
# load the furst image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length
image = cv2.imread("images/bigcamera.jpg")
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

# loop over the images

cap = cv2.VideoCapture(0)
while True:
    # load the image, find the marker in the image, then compute the
    # distance to the marker from the camera
    ret, image = cap.read()
    marker = find_marker(image)

    if marker:
        inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
        # draw a bounding box around the image and display it
        box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
        box = np.int0(box)
        cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
        cv2.putText(image, "%.2fft" % (inches / 12),
            (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
            2.0, (0, 255, 0), 3)
    cv2.imshow("image", image)
    cv2.waitKey(1)
cap.release()
