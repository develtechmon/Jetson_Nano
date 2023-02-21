import numpy as np
import cv2

def gstreamer_pipeline(
    capture_width=3280,
    capture_height=2464,
    display_width=820,
    display_height=616,
    framerate=21,
    flip_method=0,
):
    return (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), "
    "width=(int)%d, height=(int)%d, "
    "format=(string)NV12, framerate=(fraction)%d/1 ! "
    "nvvidconv flip-method=%d ! "
    "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=(string)BGR ! appsink"
    % (
        capture_width,
        capture_height,
        framerate,
        flip_method,
        display_width,
        display_height,
    )
)

#camSet = 'nvarguscamerasrc ! video/x-raw(memory:NVMM),width=3820, height=2464, framerate=21/1, format=NV12 ! nvvidconv flip-method=0 ! video/x-raw,width=960, height=616 ! nvvidconv ! nvegltransform ! nveglglessink -e'

def show_camera():
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    #cap = cv2.VideoCapture(camSet)
    if cap.isOpened():
        while True:
            success, img = cap.read()
            cv2.imshow("Capture", img)
            if cv2.waitKey(1) & 0XFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")
    
#    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
#    print(gstreamer_pipeline(flip_method=0))
#    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
#    if cap.isOpened():
#        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
#        # Window
#        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
#            ret_val, img = cap.read()
#            cv2.imshow("CSI Camera", img)
#            # This also acts as
#            keyCode = cv2.waitKey(30) & 0xFF
#            # Stop the program on the ESC key
#            if keyCode == 27:
#                break
#        cap.release()
#        cv2.destroyAllWindows()
#    else:
#        print("Unable to open camera")


if __name__ == "__main__":
    show_camera()
    
