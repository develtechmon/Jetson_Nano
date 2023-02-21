#!/usr/bin/python3

import jetson.inference
import jetson.utils
import cv2
import time
import numpy as np
from csi_camera import CSI_Camera

font=cv2.FONT_HERSHEY_SIMPLEX
dispW=1280
dispH=720
DISPLAY_WIDTH=640
DISPLAY_HEIGHT=360
SENSOR_MODE_720=3
timeStamp=time.time()
fpsFilt=0
show_fps = True

net = jetson.inference.detectNet("SSD-Mobilenet-v2", threshold=0.5)

def gstreamer_pipeline(
    sensor_id=0,
    sensor_mode=3,
    capture_width=3280,
    capture_height=2464,
    display_width=640,
    display_height=360,
    framerate=21,
    flip_method=0,
):
    return (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), "
    "width=(int)%d, height=(int)%d, "
    "format=(string)NV12, framerate=(fraction)%d/1 ! "
    "nvvidconv flip-method=%d ! "
    "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=(string)BGR ! appsink"
    % (
        capture_width,
        capture_height,
        framerate,
        flip_method,
        display_width,
        display_height,
    )
)

def read_camera(csi_camera,display_fps):
    _ , camera_image=csi_camera.read()
    #if display_fps:
    #    draw_label(camera_image, "Frames Displayed (PS): "+str(csi_camera.last_frames_displayed),(10,20))
    #    draw_label(camera_image, "Frames Read (PS): "+str(csi_camera.last_frames_read),(10,40))
    return camera_image 
  
#cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
#cap.set(cv2.CAP_PROP_FPS,30)

#cap = cv2.VideoCapture('/dev/video1')
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

def show_camera():    
    left_camera = CSI_Camera()
    left_camera.create_gstreamer_pipeline(
            sensor_id=0,
            sensor_mode=SENSOR_MODE_720,
            framerate=30,
            flip_method=0,
            display_height=DISPLAY_HEIGHT,
            display_width=DISPLAY_WIDTH,
    )
    left_camera.open(left_camera.gstreamer_pipeline)
    left_camera.start()
    #cv2.namedWindow("Face Detect", cv2.WINDOW_AUTOSIZE)

    if (
        not left_camera.video_capture.isOpened()
        ):
        # Cameras did not open, or no camera attached

        print("Unable to open any cameras")
        # TODO: Proper Cleanup
        SystemExit(0)

    while True:
        #success,img = cap.read()
        img=read_camera(left_camera,False)
        height = img.shape[0]
        width = img.shape[1]
        
        #COLOR_BGR2RGBA
        frame=cv2.cvtColor(img,cv2.COLOR_BGR2RGBA).astype(np.float32)
        frame=jetson.utils.cudaFromNumpy(frame)
        
        detections = net.Detect(frame, width, height)
        for detect in detections:
            ID=detect.ClassID
            top=int(detect.Top)
            left=int(detect.Left)
            bottom=int(detect.Bottom)
            right=int(detect.Right)
            item=net.GetClassDesc(ID)
            
            print(item)
            
            if (item=="person"):
                cv2.rectangle(img,(left,top),(right,bottom),(0,255,0),3)
                cv2.putText(img,item,(left,top+20),font,.95,(248, 254, 0),2)  
                
        cv2.imshow("Capture", img)
        #cv2.moveWindow('Capture',0,0)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break
        
    left_camera.stop()
    #left_camera.release()
  #  cv2.destroyAllWindows()

if __name__ == "__main__":
    dt=time.time()-timeStamp
    timeStamp=time.time()
    fps=1/dt
    fpsFilt=.9*fpsFilt + .1*fps
    show_camera()
    cv2.putText(img,str(round(fpsFilt,1))+' fps',(0,30),font,1,(112, 254, 0),2)

   #Not finsished
cv2.destroyAllWindows()

        
    
    