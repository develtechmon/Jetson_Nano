from time import sleep
import time
from datetime import datetime
import numpy as np
import threading
import state
#import cv2

class Core(threading.Thread):
    def __init__(self,drone,alt,det,pid,perror,writer,img,id,info):
        threading.Thread.__init__(self)
        self.daemon = True

        self.altitude = alt
        self.drone = drone
        self.det = det
        self.pid = pid
        self.pError = perror
        #self.writer = writer

        self.img = img
        self.id = id
        self.info = info

    def takeoff(self):
        self.drone.control_tab.armAndTakeoff(self.altitude)
        state.set_system_state("search")
    
    def search(self,id):
        start = time.time()
        self.drone.control_tab.stop_drone(self.altitude)
        while time.time() - start < 60:
            if (id == 1):
                state.set_system_state("track")
        state.set_system_state("land")
    
    def track(self,info):
        if (info[1]) != 0:
            state.set_airborne("on")
            self.det.track.trackobject(info,self.pid,self.pError,self.altitude)
            
        else:
            state.set_system_state("search")
            state.set_time(60)
    
    def run (self):
        while True:

            # img,id,info = self.det.captureimage_non_csi()

            if (state.get_system_state() == "takeoff"):
                self.takeoff()

            elif (state.get_system_state() == "search"):
                self.search(self.id)
            
            elif(state.get_system_state() == "track"):
                self.track(self.info)

            elif (state.get_system_state() == "land"):
                #self.writer.release()
                self.drone.control_tab.land()

            elif (state.get_system_state() == "end"):
                state.set_system_state("takeoff")
                state.set_airborne("off")

                print("Waiting to change to GUIDED Mode")
            
                while not self.drone.vehicle.mode.name == "GUIDED":
                    sleep(1)
                #self.writer = self.record()
            
            #cv2.imshow("output",img)
            #self.writer.writer(self.img)

            #if cv2.waitKey(1) & 0XFF == ord('q'):
            #    break

        #self.writer.release()
        #cv2.destroyAllWindows()
        



        
