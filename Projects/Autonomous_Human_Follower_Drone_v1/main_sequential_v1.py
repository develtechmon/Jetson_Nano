import cv2
import state
import subprocess
import queue

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
from buzzer import *

STATE = "takeoff" 

os.system ('echo 2328 | sudo -S systemctl restart nvargus-daemon')
os.system ('echo 2328 | sudo -S chmod 666 /dev/ttyTHS1')

pError   = 0
altitude = 1.5

# 1st Option 
#pid      = [0.1,0.1]

# 2nd Option
pid     = [0.3,0.1]

# 3rd Option
#pid     = [0.5,0.4]

def takeoff():
    drone.control_tab.armAndTakeoff(altitude)
    state.set_system_state("search")
    
def search(id):
    start = time.time()
    drone.control_tab.stop_drone(altitude)
    while time.time() - start < 60:
        if (id == 1):
            state.set_system_state("track")
    state.set_system_state("land")
    
def track(info):
    if (info[1]) != 0:
        state.set_airborne("on")
        det.track.trackobject(info,pid,pError,altitude)

    else:
        state.set_system_state("search")

def write_video(frame_queue):
    curr_timestamp = int(datetime.timestamp(datetime.now()))
    path = "/home/jlukas/Desktop/My_Project/Jetson_Nano/Projects/Autonomous_Human_Follower_Drone_v1/record/"
    out = cv2.VideoWriter(path + "record" + str(curr_timestamp) + '.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 10 ,(cam.DISPLAY_WIDTH,cam.DISPLAY_HEIGHT))
    
    while True:
        #Get the next frame from the queue
        frame = frame_queue.get()

        # If we recieve None, we're done
        if frame is None:
            break

        # Write the frame to the output video
        out.write(frame)

    # Release the VideoWriter
    out.release()


def core_run(img,id,info):
    if (state.get_system_state() == "takeoff"):
        takeoff()

    elif (state.get_system_state() == "search"):
        search(id)

    elif (state.get_system_state() == "track"):
        track(info)

    elif (state.get_system_state() == "land"):
        drone.control_tab.land()
        frame_queue.put(None)
        
        alarm()
        
    elif (state.get_system_state() == "end"):
        state.set_system_state("takeoff")
        state.set_airborne("off")
            
        print("Waiting to change to GUIDED Mode")
            
        while not drone.vehicle.mode.name == "GUIDED":
            sleep(1)
        
        rec = threading.Thread(target=write_video, args=(frame_queue,))
        rec.start()

# Create a queue to hold the frames
frame_queue = queue.Queue()

# Create a new thread to write the video
rec = threading.Thread(target=write_video, args=(frame_queue,))
rec.start()

if __name__ == "__main__":
    
    while True:
        try:
            drone = Drone()
            break
        
        except Exception as e:
            sleep(2)
    
    # Initialize CSI Camera
    cam = Camera()

    # Initialize non CSI Camera
    #cam = Camera()
        
    #Initialize Detector
    det = Detect(cam,drone)
    
    #Initialize Lidar
    lidar = Lidar(drone, altitude)
    lidar.start()
    
    #Initialize state
    state.set_system_state("takeoff")
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
        core_in = threading.Thread(target=core_run,daemon=True, args=(img,id,info,))
        core_in.start()
                
        #det.track.visualise(img)   

        frame_queue.put(img)

        cv2.imshow("Output",img)
                
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break
    
    # Add a None to the queue to signal the end of the video
    frame_queue.put(None)

    # Finish the record thread
    rec.join()     

    #writer.release()
    cv2.destroyAllWindows()
            
            
