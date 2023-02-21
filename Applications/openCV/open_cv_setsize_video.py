#from picamera import PiCamera
import cv2
from time import sleep

#camera = PiCamera()

print("Package Imported")

cap = cv2.VideoCapture(0)

cap.set(3,800) ##--------->Width is 800 with Id = 3
cap.set(4,800) ##--------->Height is 800 with Id = 4
cap.set(10,100) ##-------->Brighhtness is 100 with Id = 10

while True:
    success, img = cap.read()
    cv2.imshow("Capture", img)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
