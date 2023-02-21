import numpy as np
import jetson.inference
import jetson.utils
from person_followingrobot_cameraThread_improvement import *
import SerialModule as sm
import cv2

class personFollowingRobotFunction():
    def __init__(self):
        self.video_source     = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink'
        self.video_getter     = VideoGet(self.video_source).start()
        self.net              = jetson.inference.detectNet("SSD-Mobilenet-v2", threshold=0.3)
        self.ser              = sm.initConnection('/dev/ttyACM0',9600)
        self.font             = cv2.FONT_HERSHEY_SIMPLEX
        self.DISPLAY_WIDTH    = 1280
        self.DISPLAY_HEIGHT   = 720
        self.SENSOR_MODE_720  = 3
  
                  
    def readImage(self):
        img = self.video_getter.frame
        return img
        
    def drawOverlays(self,img):
        # Draw black rectangle bottom
        cv2.rectangle(img, (0, self.DISPLAY_HEIGHT-24), (self.DISPLAY_WIDTH,self.DISPLAY_HEIGHT), (0,0,0), -1)
        
        # Draw center middle line
        cv2.line(img,(self.DISPLAY_WIDTH//2,0),(self.DISPLAY_WIDTH//2,self.DISPLAY_HEIGHT-24), (255,0,255),3)    
        return img
    
    def captureimage(self,img): 
        self.myobjectListC    = []
        self.myobjectListArea = []
        
        height = img.shape[0]
        width  = img.shape[1]
        frame  = cv2.cvtColor(img,cv2.COLOR_BGR2RGBA).astype(np.float32)
        frame  = jetson.utils.cudaFromNumpy(frame)

        detections = self.net.Detect(frame, height, width)
        for detect in detections:
            self.ID=detect.ClassID
            self.top=int(detect.Top)
            self.left=int(detect.Left)
            self.bottom=int(detect.Bottom)
            self.right=int(detect.Right)
            #widths = detection.Width
            self.area = int(detect.Area)
            self.location = detect.Center
            self.item=self.net.GetClassDesc(self.ID)
            
            self.cx = self.location[0]
            self.cy = self.location[1]
            self.myobjectListArea.append(self.area)
            self.myobjectListC.append([self.cx,self.cy])
            
        if len(self.myobjectListArea) !=0:
            if self.ID==1:
                cv2.rectangle(img,(self.left,self.top),(self.right,self.bottom),(0,255,0),7)
                cv2.line(img, (self.DISPLAY_WIDTH//2, int(self.cy)), (int(self.cx),int(self.cy)), (0,0,255),5)
                cv2.putText(img,"Lukas",(self.left,self.top-10),self.font,.95,(255, 0, 0),3)
                cv2.putText(img,"Tracking",(10,self.DISPLAY_HEIGHT- 8),self.font,0.5,(150,150,255),2)

                i = self.myobjectListArea.index(max(self.myobjectListArea))
                return [self.myobjectListC[i],self.myobjectListArea[i]]
            
            #else:
            #    return [[0,0],0]
        else:
            return [[0,0],0]
        
    def trackObject(self,info, pError,pid):
        if info is not None:                        
        #if int(info[1]) !=0:
            error  = self.DISPLAY_WIDTH//2 - info[0][0]
            posX   = int(pid[0]*error + pid[1]*(error - pError))
            posX   = int(np.interp(posX, [-self.DISPLAY_WIDTH//4, self.DISPLAY_WIDTH//4], [-35,35]))
            pError = error
            #print("----" + str(posX) + "---" + str(error))
            
            sm.sendData(self.ser, [50, posX],4) #-->arduinoConnection, staticSpeed, PIDValue, 4 digit
        
        else:
            sm.sendData(self.ser,[0,0],4)
            
   
            
            
            
            
 

        

                
                
            
         
        


    
    
        
