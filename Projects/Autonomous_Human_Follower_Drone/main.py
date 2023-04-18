import cv2
import queue
import sys
import os
import threading
import state
import subprocess
import RPi.GPIO as GPIO

from time import sleep,time
from datetime import datetime
from sys import exit

from detect import *
from camera import *
from track import *
from config import *
from lidar import *
from buzzer import *

os.system ('echo 2328 | sudo -S systemctl restart nvargus-daemon')
os.system ('echo 2328 | sudo -S chmod 666 /dev/ttyTHS1')

pError   = 0
altitude = 1.5

# buzzer=19

# 1st Option 
pid      = [0.1,0.1]

# 2nd Option
#pid     = [0.3,0.1]

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

# def record():
#     curr_timestamp = int(datetime.timestamp(datetime.now()))
#     path = "/home/jlukas/Desktop/My_Project/Jetson_Nano/Projects/Autonomous_Human_Follower_Drone/record/"
#     writer= cv2.VideoWriter(path + "record" + str(curr_timestamp) + '.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 10 ,(cam.DISPLAY_WIDTH,cam.DISPLAY_HEIGHT))
#     return writer

def write_video(frame_queue):
    curr_timestamp = int(datetime.timestamp(datetime.now()))
    path = "/home/jlukas/Desktop/My_Project/Jetson_Nano/Projects/Autonomous_Human_Follower_Drone/record/"
    out = cv2.VideoWriter(path + "record" + str(curr_timestamp) + '.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 10 ,(cam.DISPLAY_WIDTH,cam.DISPLAY_HEIGHT))
    
    #out = record()

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
    
    # GPIO.setmode(GPIO.BOARD)
    # GPIO.setup(buzzer, GPIO.OUT, initial=GPIO.LOW)

    cam = Camera()

    #writer = record()

    det   = Detect(cam,drone)
    
    lidar = Lidar(drone,altitude)
    lidar.start()

    state.set_system_state("takeoff")
    state.set_airborne("off")

    while drone.is_active:
        try:       
            img, id, info = det.captureimage()   
            #det.track.visualise(img)    
                        
            if (state.get_system_state() == "takeoff"):
                off = threading.Thread(target=takeoff, daemon=True)
                off.start()
            
            elif(state.get_system_state() == "search"):
                sea = threading.Thread(target=search, daemon=True, args=(id,))
                sea.start()
                
            elif(state.get_system_state() == "track"):
                tra = threading.Thread(target=track, daemon=True, args=(info,))
                tra.start()
                        
            elif(state.get_system_state() == "land"):
                drone.control_tab.land()

                #cv2.destroyAllWindows()
                #writer.release()
                frame_queue.put(None)

                alarm()

                # GPIO.output(buzzer,GPIO.HIGH)
                # sleep(2)
                # GPIO.output(buzzer,GPIO.LOW)
                # sleep(1)

            elif(state.get_system_state() == "end"):
                state.set_system_state("takeoff")
                state.set_airborne("off")
                
                print("Waiting to change to GUIDED Mode")
                
                while not drone.vehicle.mode.name == "GUIDED":
                    sleep(1)

                #writer = record()
                rec = threading.Thread(target=write_video, args=(frame_queue,))
                rec.start()
            
            frame_queue.put(img)

            cv2.imshow("Capture",img)
            #writer.write(img)

            if cv2.waitKey(1) & 0XFF == ord('q'):
               #os.system("echo 2328 | sudo -S pkill -9 -f main.py")
               break
            
        except Exception as e:
            print(str(e))

    # Add a None to the queue to signal the end of the video
    frame_queue.put(None)

    # Finish the record thread
    rec.join()     

    #writer.release()
    cv2.destroyAllWindows()

    # Method 1 to terminate process
    #process = subprocess.call('/home/jlukas/Desktop/My_Project/Autonomous_Human_Follower_Drone/csh/end') 

    # Method 2 to terminate process
    #os.system("echo 2328 | sudo -S pkill -9 -f main.py")
       
    
