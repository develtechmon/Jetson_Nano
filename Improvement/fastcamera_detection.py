from csi_camera import CSI_Camera
import cv2
import numpy as np

show_fps = True

class faceCam():
    
    def __init__(self):
        self.DISPLAY_WIDTH    = 640
        self.DISPLAY_HEIGHT   = 360
        self.SENSOR_MODE_1080 = 2
        self.SENSOR_MODE_720  = 3
        
    def initializeCamera(self):
        self.face_cascade = cv2.CascadeClassifier("/home/jlukas/Desktop/My_Project/resources/Cascades/haarcascade_frontalface_default.xml")
        self.cam = CSI_Camera()
        self.cam.create_gstreamer_pipeline(
            sensor_id=0,
            sensor_mode=self.SENSOR_MODE_720,
            framerate=30,
            flip_method=0,
            display_height=self.DISPLAY_HEIGHT,
            display_width=self.DISPLAY_WIDTH,    
        )
        self.cam.open(self.cam.gstreamer_pipeline)
        self.cam.start()
        cv2.namedWindow("Face Detect", cv2.WINDOW_AUTOSIZE)
        
        if (not self.cam.video_capture.isOpened()):
            print("Unable to open any camera")
            SystemExit(0)
            
    def readCamera(self,csiCam,displayFPS):
        _, camImage = csiCam.read()
        return camImage
    
    def faceDetection(self):
        try:
            self.cam.start_counting_fps()
            while True:
                img = self.readCamera(self.cam, False)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:               
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    roi_gray = gray[y : y + h, x : x + w]
                    roi_color = img[y : y + h, x : x + w]
                
                cv2.imshow("Face Detect",img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self.cam.stop()
            self.cam.release()
            cv2.destroyAllWindows()
                   
if __name__ == "__main__":
    detect = faceCam()
    
    initCamera = detect.initializeCamera()
    faceDetect = detect.faceDetection()
    
    
    
        
    