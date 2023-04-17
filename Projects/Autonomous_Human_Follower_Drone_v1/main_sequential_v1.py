import cv2
import state
import subprocess
import RPi.GPIO as GPIO
import os
from time import sleep,time
from datetime import datetime
from sys import exit

from core import *
from detect import *

from camera import *
#from camera_non_thread import *

from track import *
from config import *
from lidar import *

STATE = "takeoff" 

os.system ('echo 2328 | sudo -S systemctl restart nvargus-daemon')
os.system ('echo 2328 | sudo -S chmod 666 /dev/ttyTHS1')

pError   = 0
altitude = 1.5

buzzer=19

# 1st Option 
#pid      = [0.1,0.1]

# 2nd Option
pid     = [0.3,0.1]

# 3rd Option
#pid     = [0.5,0.4]

def takeoff():
    drone.control_tab.armAndTakeoff(altitude)
    #state.set_system_state("search")
    return "search"
    
def search(id):
    start = time.time()
    drone.control_tab.stop_drone(altitude)
    while time.time() - start < 60:
        if (id == 1):
            return "track"
            #state.set_system_state("track")
    
    #state.set_system_state("land")
    return "land"
    
def track(info):
    if (info[1]) != 0:
        state.set_airborne("on")
        det.track.trackobject(info,pid,pError,altitude)

    else:
        #state.set_system_state("search")
        return "search"

def record():
    curr_timestamp = int(datetime.timestamp(datetime.now()))
    path = "/home/jlukas/Desktop/My_Project/Jetson_Nano/Projects/Autonomous_Human_Follower_Drone_v1/record/"
    writer= cv2.VideoWriter(path + "record" + str(curr_timestamp) + '.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30 ,(cam.DISPLAY_WIDTH,cam.DISPLAY_HEIGHT))
    return writer

def write(frame,writer):
    writer.write(frame)

def core_run(img,id,info,writer):
    if (STATE == "takeoff"):
    #if (state.get_system_state() == "takeoff"):
        takeoff()

    elif (STATE == "search"):
    #elif (state.get_system_state() == "search"):
        search(id)

    elif (STATE == "track"):
    #elif (state.get_system_state() == "track"):
        track(info)

    elif (STATE == "land"):
    #elif (state.get_system_state() == "land"):
        writer.release()
        drone.control_tab.land()
        GPIO.output(buzzer,GPIO.HIGH)
        sleep(1)
        GPIO.output(buzzer,GPIO.LOW)
        sleep(1)
        
    elif (state.get_system_state() == "end"):
        #state.set_system_state("takeoff")
        STATE = "takeoff"
        state.set_airborne("off")
            
        print("Waiting to change to GUIDED Mode")
            
        while not drone.vehicle.mode.name == "GUIDED":
            sleep(1)
        writer = record()
    
if __name__ == "__main__":
    
    while True:
        try:
            drone = Drone()
            break
        
        except Exception as e:
            sleep(2)
    
    # Intialize Buzzer
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buzzer,GPIO.OUT, initial=GPIO.LOW)

    # Initialize CSI Camera
    cam = Camera()

    # Initialize non CSI Camera
    #cam = Camera()
    
    #Intialize Recorder
    writer = record()
    
    #Initialize Detector
    det = Detect(cam,drone)
    
    #Initialize Lidar
    lidar = Lidar(drone, altitude)
    lidar.start()
    
    #Initialize state
    #state.set_system_state("takeoff")
    state.set_airborne("off")
    while drone.is_active:

        # Capture Image and perform detection
        img, id, info = det.captureimage_csi()

        # Capture Image using non-csi
        #img,id,info = det.captureimage_non_csi()

        # Search and Track run using separate thread or class (?).
        # Using Class Thread 
        #core = Core(drone,altitude,det,pid,pError,writer,img,id,info)
        #core.start()

        # Using Thread
        core_in = threading.Thread(target=core_run,daemon=True, args=(img,id,info,writer))
        core_in.start()
                
        #det.track.visualise(img)   

        cv2.imshow("Output",img)
        
        #record = threading.Thread(target=write,daemon=True,args=(img,writer,))
        #record.start()

        #writer.write(img)
        
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break
    
    writer.release()
    cv2.destroyAllWindows()
            
            
