import cv2
from statistics import median

def callibrate(img_path, known_width, known_distance):
    img = cv2.imread(img_path)
    face = find_face(img)
    return face[2] * known_distance / known_width

def find_face(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 8)
    for face in faces:
        return face

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
            for i in range(5):
                _, frame = cap.read()
                if frame is not None:
                    face = find_face(frame)
                    if face is not None:
                        dists.append(self.distance_to_camera(face[2]))
                else:
                    print(f"Frame Error: {self.device_ind}")
            if len(dists) > 0:
                self.current_distance = median(dists)
        else:
            print(f"Cap Error: {self.device_ind}")
        if not self.always_on:
            cap.release()

c = Camera(0)
while True:
    c.update_distance()
    print(c.current_distance)
