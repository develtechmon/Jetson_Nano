import jetson.inference
import jetson.utils
import cv2
import numpy as np
from engines import *

#class Track(threading.Thread):
class Track:
    def __init__(self,cam,D):
        # threading.Thread.__init__(self)
        self.daemon  = True
        self.w       = cam.DISPLAY_WIDTH
        self.h       = cam.DISPLAY_HEIGHT  
        self.engine  = D.engines 
        self.control = D.control_tab
         
    def trackobject(self,info,pid,pError,altitude):
        self.info   = info
        self.pid    = pid
        self.pError = pError
        
        if ((self.info[1]) !=0):
            error = self.w/2 - self.info[0][0]
            self.posXC   = (self.pid[0]*error + self.pid[1]*(error-self.pError))
            
            # 2nd Option
            self.posX  = (np.interp(self.posXC, [-self.w//4, self.w//4], [-40,40]))
            
            # 1st Option
            #self.posX   = (np.clip(self.posXC, -15, 15))
               
            self.pError = error
            
            #print(error)
            #print(str(self.posX))
            
            self.engine.executeChangesNow(0.2,0,altitude)
            self.engine.send_movement_command_YAW(self.posX)
            
            # 1st Method of PID
            #self.control.set_XDelta(self.posX)
            #self.control.control_drone()
                            
        else:
            self.engine.executeChangesNow(0,0,altitude)
            self.engine.send_movement_command_YAW(0)
            
            # 1st Method of PID
            #self.control.set_XDelta(0)
            #self.control.control_drone()
                   
    def visualise(self,img):
         # Top
        cv2.rectangle(img, (0,0), (self.w,24), (0,0,0), -1)

        # Bottom
        cv2.rectangle(img, (0, self.h-24), (self.w,self.h), (0,0,0), -1)
        
         # Width and Height
        text_dur = 'Width : {} Height: {}'.format(self.w, self.h)
        cv2.putText(img, text_dur, (10,16), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (150,150,255), 2)
        
        

        
            
        
    
