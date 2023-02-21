from person_followingrobot_function_improvement import *
from flask import Flask, Response, render_template
#from PIL import Image
import threading
import os
import time

pError = 0
pid = [0.5,0.4]
os.system ('sudo systemctl restart nvargus-daemon')

if __name__ == '__main__':
    camera = personFollowingRobotFunction()        

    while True:        
        #Step 1 - Read Image
        img = camera.readImage()
        
        #Step 2 - Draw Overlays
        draw = camera.drawOverlays(img)
        
        #Step 3
        info = camera.captureimage(img)       
        
        #Step 4
        result = camera.trackObject(info,pError, pid)
                
        #cv2.imshow("Frame",img)
        if cv2.waitKey(1) & 0XFF==ord('q'):
            break


    #camera.stop()
    cv2.destroyAllWindows()
