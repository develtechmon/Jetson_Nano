import threading
import cv2
import queue
from datetime import datetime
import keyboard as kp

output_path = r"C:/Users/jlukas/Desktop/My_Projects/to_upload/Jetson_Nano/Projects/Autonomous_Human_Follower_Drone/record/"

cap = cv2.VideoCapture(0)

def record():
    curr_timestamp = int(datetime.timestamp(datetime.now()))
    writer= cv2.VideoWriter(output_path + "record" + str(curr_timestamp) + '.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30 ,(640,480))
    return writer

def write_video(frame_queue):
    # Define the codec and create VideoWriter object
    curr_timestamp = int(datetime.timestamp(datetime.now()))
    out= cv2.VideoWriter(output_path + "record" + str(curr_timestamp) + '.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30 ,(640,480))

    #out = record()
    
    while True:
        # Get the next frame from the queue
        frame = frame_queue.get()

        # If we receive None, we're done
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

# Loop over frames and add them to the queue
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If the frame is None, we're done
    if frame is None:
        break

    # Add the frame to the queue
    frame_queue.put(frame)
    
    # Show the image
    cv2.imshow("Output", frame)

    if cv2.waitKey(1) & 0XFF == ord('q'):
        break

    elif kp.is_pressed('w'):
        frame_queue.put(None)

    elif kp.is_pressed('l'):
        rec = threading.Thread(target=write_video, args=(frame_queue,))
        rec.start()

# Add a None to the queue to signal the end of the video
frame_queue.put(None)

# Wait for the thread to finish
rec.join()

#writer.release()
cv2.destroyAllWindows()
