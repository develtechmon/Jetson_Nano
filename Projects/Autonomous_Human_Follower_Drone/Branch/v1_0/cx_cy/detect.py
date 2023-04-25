import jetson.inference
import jetson.utils
from track import *
import numpy as np
import cv2
from csi_camera import CSI_Camera

import numpy as np

class Detect:
    def __init__(self,cam,D):
        self.c      = cam.initializecamera()
        self.net    = cam.net
        self.w      = cam.DISPLAY_WIDTH
        self.h      = cam.DISPLAY_HEIGHT
        self.f      = cam.font

        self.track  = Track(cam,D)
        
    def read_camera(self,csi_camera,display_fps):   
        _ , camera_image=csi_camera.read()
        return camera_image 
    
    def readimage(self):
        return self.read_camera(self.c,True)
      
    def captureimage(self):
        while True:     
            #myobjectlistC = []
            #myobjectlistArea = []
            
            myobjectlistC = np.array([])
            myobjectlistArea = np.array([])

            img        = self.read_camera(self.c,True)
            height     = img.shape[0]
            width      = img.shape[1]
            frame      = cv2.cvtColor(img,cv2.COLOR_BGR2RGBA).astype(np.float32)
            frame      = jetson.utils.cudaFromNumpy(frame)
            detections = self.net.Detect(frame, width, height)
            
            ID = None
            for detect in detections:
                ID       = detect.ClassID
                top      = int(detect.Top)
                left     = int(detect.Left)
                bottom   = int(detect.Bottom)
                right    = int(detect.Right)
                area     = int(detect.Area)
                location = detect.Center
                
                item = self.net.GetClassDesc(ID)
                user = "Luke"
                cx   = location[0]
                cy   = location[1]

                # Using Numpy
                myobjectlistArea = np.append(myobjectlistArea,area)
                myobjectlistC = np.append(myobjectlistC,[cx,cy])
                
                # Using List
                #myobjectlistArea.append(area)
                #myobjectlistC.append([cx,cy])
		                
                if len(myobjectlistArea) !=0:
                    if ID==1:
                        cv2.rectangle(img,(left,top),(right,bottom),(0,255,0),3)
                        cv2.circle(img, (int(cx), int(cy)), 10, (0, 0, 255), thickness=-1, lineType=8, shift=0)
                        cv2.line(img, (self.w//2, int(cy)), (int(cx),int(cy)), (255,0,255),3)
                        cv2.putText(img,user,(left+3,top-10),self.f,.95,(248, 254, 0),3)
                                                                        
                        info = ([myobjectlistC, myobjectlistArea])
                        
                        print("\ninfo >> ", info)
                        print("Cx >> ", info[0][0])
                        print("Cy >> ", info[0][1])
                        print("Area >> ", info[1])
                        
                        # List
                        #i = myobjectlistArea.index(max(myobjectlistArea))
                        #return img, ID,[myobjectlistC[i],myobjectlistArea[i]]

                        # Numpy
                        #i = np.argmax(myobjectlistArea)
                        #return (img, ID,[[myobjectlistC[i], myobjectlistC[i+1]], myobjectlistArea[i]])
                        
                        # Cx only
                        return (img, ID, cx)
        
                else:
                    #return img, ID,[[0,0],0]
                    return (img, ID, 0)
            
            
                

            
        
  
