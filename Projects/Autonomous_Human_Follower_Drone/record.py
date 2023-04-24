import cv2
from time import sleep,time
from datetime import datetime

def write_video(frame_queue):
    curr_timestamp = int(datetime.timestamp(datetime.now()))
    path = "/home/jlukas/Desktop/My_Project/Jetson_Nano/Projects/Autonomous_Human_Follower_Drone/record/"
    out = cv2.VideoWriter(path + "record_queue" + str(curr_timestamp) + '.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 10 ,(640,480))
    
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
