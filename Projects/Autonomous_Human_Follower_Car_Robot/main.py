from csi_camera import CSI_Camera
from detect import *
from camera import *
from track import *
import cv2
import os

os.system ('sudo systemctl restart nvargus-daemon')

pError   = 0
pid      = [0.5,0.4]

if __name__ == "__main__":
    cam = Camera()
    det = Detect(cam) 
    while True:
        img,info = det.captureimage()
        
        det.track.trackobject(info,pid,pError)

        det.track.visualise(img)
        
        cv2.imshow("Capture",img)
        
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break
    cv2.destroyAllWindows()
        
        
    